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
    async def create_receipt(
        cls, data: dict = {}
    ) -> Optional[ReceiptWithPositionsResponse]:
        positions = data.pop("positions", [])

        receipt: Receipt = await cls.add(
            {
                **data,
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

        if positions is not None:
            await PositionCheckDAO.delete({"check_id": filter_by["id"]})
            for position_num, position in enumerate(positions):
                await PositionCheckDAO.add(
                    {
                        **position,
                        "owner_id": receipt.owner_id,
                        "check_id": receipt.id,
                        "position": position_num + 1,
                    }
                )

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
