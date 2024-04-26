import datetime
from typing import Optional

from sqlalchemy import Select, and_, select, true

import position_check.utils as position_utils
from check.models import Receipt
from check.schemas import ReceiptResponse, ReceiptStatus, ReceiptWithPositionsResponse
from check.utils import change_format
from dao.base import BaseDAO
from database import async_session_maker
from position_check.dao import PositionCheckDAO
from position_check.models import PositionCheck
from position_check.schemas import PositionResponse
from pprint import pprint

class CheckDAO(BaseDAO):
    model = Receipt

    @classmethod
    async def get_one_receipt(
        cls, filter_by: dict = {}
    ) -> Optional[ReceiptWithPositionsResponse]:
        receipt: Receipt = await cls.get_one_or_none(filter_by)

        return (
            ReceiptWithPositionsResponse(
                positions=await PositionCheckDAO.get_all_positions(
                    {"check_id": receipt.id}
                ),
                **receipt.__dict__,
            )
            if receipt is not None
            else None
        )

    # @classmethod
    # async def get_all_receipts(cls, filter_by: dict = {}) -> dict:
    #     checks: list[Receipt] = await cls.get_all(filter_by)

    #     return [ReceiptResponse(**check.__dict__) for check in checks]

    @classmethod
    async def get_all_receipts(
        cls, filter_by: dict = {}
    ) -> list[ReceiptWithPositionsResponse]:
        time_start = filter_by.pop("time_start", None)
        time_end = filter_by.pop("time_end", None)
        count = filter_by.pop("count", None)

        if count is None:
            count = 100000000

        async with async_session_maker() as session:
            query: Select = (
                select(cls.model)
                .filter_by(
                    **filter_by,
                )
                .where(and_((cls.model.date > time_start) if time_start else true()))
                .where(and_((cls.model.date < time_end)) if time_end else true())
            )

            receipts: list[Receipt] = [
                row[0] for row in (await session.execute(query)).fetchall()
            ]
            receipts.sort(key=lambda check: check.date, reverse=True)

            return [
                ReceiptWithPositionsResponse(
                    positions=(
                        await PositionCheckDAO.get_all_positions(
                            {"check_id": receipt.id}
                        )
                    ),
                    **receipt.__dict__,
                )
                for receipt in receipts[:count]
            ]

    @classmethod
    async def get_last_receipts(
            cls, filter_by: dict = {}
    ) -> Optional[ReceiptWithPositionsResponse]:

        async with async_session_maker() as session:
            query: Select = (
                select(cls.model)
                .filter_by(
                    **filter_by,
                )
                .order_by(Receipt.number.desc())
                .limit(1)
            )

            receipt = await session.execute(query)
            receipt = receipt.scalar()

            return [
                ReceiptWithPositionsResponse(
                    positions=(
                        await PositionCheckDAO.get_all_positions(
                            {"check_id": receipt.id}
                        )
                    ),
                    **receipt.__dict__,
                )
            ]

    @classmethod
    async def create_receipt(
        cls, data: dict = {}
    ) -> Optional[ReceiptWithPositionsResponse]:
        positions = data.pop("positions", [])
        last_receipt: ReceiptWithPositionsResponse = await cls.get_last_receipts(
            {"owner_id": data.get('owner_id'),
             "organization_id": data.get('organization_id'),
             "store_id": data.get('store_id')
            })
        if data.get("type_operation") == 2:
            sell_receipt: ReceiptWithPositionsResponse = await cls.get_one_receipt(
                {"owner_id": data.get('owner_id'),
                 "organization_id": data.get('organization_id'),
                 "id": data.get('reason_id')
                 }
            )

        number_last_receipt = int(last_receipt[0].number)
        number = str(data.get("number", number_last_receipt + 1 if number_last_receipt else 1))
        # pprint(sell_receipt)

        receipt: Receipt = await cls.add(
            {
                **data,
                "number": number,
                "reasonCheckName": sell_receipt.number if data.get("type_operation") == 2 else None,
                "date": datetime.datetime.utcnow(),
                "check_status": ReceiptStatus.CREATED.value,
            }
        )
        for position_num, position in enumerate(positions):
            await PositionCheckDAO.add(
                {
                    **position,
                    "owner_id": receipt.owner_id,
                    "check_id": receipt.id,
                    "position": position_num + 1,
                }
            )

        if data.get("type_operation") == 2:
            query_params = {
                "owner_id": data.get('owner_id'),
                "organization_id": data.get('organization_id'),
                "store_id": data.get('store_id'),
                "cash_shift_id": data.get('cash_shift_id'),
                "id": data.get("reason_id")
            }
            body_params = {
                "reason_id": receipt.__dict__['id'],
                "reasonCheckName": receipt.__dict__['number']
            }
            await cls.update_receipt(query_params, body_params)

        return (
            ReceiptWithPositionsResponse(
                positions=await PositionCheckDAO.get_all_positions(
                    {"check_id": receipt.id}
                ),
                **receipt.__dict__,
            )
            if receipt is not None
            else None
        )

    @classmethod
    async def update_receipt(
        cls, filter_by: dict = {}, data: dict = {}
    ) -> Optional[ReceiptWithPositionsResponse]:
        positions = data.pop("positions", None)

        receipt: Receipt = await cls.update(
            filter_by, {**data, "date": datetime.datetime.utcnow()}
        )

        if positions:
            await PositionCheckDAO.delete({"check_id": filter_by.get('id')})
            for position_num, position in enumerate(positions):
                await PositionCheckDAO.add(
                    {
                        **position,
                        "owner_id": filter_by.get('owner_id'),
                        "check_id": filter_by.get('id'),
                        "position": position_num + 1,
                    }
                )

        return (
            ReceiptWithPositionsResponse(
                positions=await PositionCheckDAO.get_all_positions(
                    {"check_id": filter_by.get('id')}
                ),
                **receipt[0].__dict__,
            )
            if receipt is not None
            else None
        )

    @classmethod
    async def close_receipt(
        cls, filter_by: dict = {}
    ) -> Optional[ReceiptWithPositionsResponse]:
        receipts: list[Receipt] = await cls.update(
            filter_by,
            {
                "check_status": ReceiptStatus.CLOSED.value,
                "date": datetime.datetime.utcnow(),
            },
        )

        return (
            ReceiptWithPositionsResponse(
                positions=await PositionCheckDAO.get_all_positions(
                    {"check_id": receipts[0].id}
                ),
                **receipts[0].__dict__,
            )
            if len(receipts) > 0
            else None
        )

    @classmethod
    async def remove_receipt(
        cls, filter_by: dict = {}
    ) -> Optional[ReceiptWithPositionsResponse]:
        positions: list[PositionResponse] = await PositionCheckDAO.get_all_positions(
            {"check_id": filter_by["id"]}
        )

        receipts: list[Receipt] = await cls.delete(filter_by)

        return (
            ReceiptWithPositionsResponse(
                positions=positions,
                **receipts[0].__dict__,
            )
            if len(receipts) > 0
            else None
        )
