import datetime
from typing import Optional

from sqlalchemy import Select, and_, select, true, cast, INTEGER
import logging
import position_check.utils as position_utils
from cash_shift.models import CashShift

from cash_shift.schemas import CashShiftWithReceiptsResponse
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
        # print(filter_by)
        async with async_session_maker() as session:
            query: Select = (
                select(cls.model)
                .filter_by(
                    **filter_by,
                )
                .order_by(cast(Receipt.number, INTEGER).desc())
                .limit(1)
            )

            receipt = await session.execute(query)
            receipt = receipt.scalar()
            # print(receipt)
            return (
                ReceiptWithPositionsResponse(
                    positions=(
                        await PositionCheckDAO.get_all_positions(
                            {"check_id": receipt.id}
                        )
                    ),
                    **receipt.__dict__,
                )
                if receipt is not None
                else None
            )

    @classmethod
    async def create_receipt(
        cls, data: dict = {}
    ) -> Optional[ReceiptWithPositionsResponse]:
        positions = data.pop("positions", [])

        # print(data.get('workplace_id'))
        # print(data.get('organization_id'))
        last_receipt: ReceiptWithPositionsResponse = await cls.get_last_receipts(
            {"owner_id": data.get('owner_id'),
             "organization_id": data.get('organization_id'),
             "store_id": data.get('store_id'),
             "workplace_id": data.get('workplace_id')
            })

        if data.get("type_operation") == 2:
            sell_receipt: ReceiptWithPositionsResponse = await cls.get_one_receipt(
                {
                    "owner_id": data.get('owner_id'),
                    "organization_id": data.get('organization_id'),
                    "id": data.get('reason_id')
                }
            )
        # number_last_receipt = int(last_receipt.number)
        number = str(data.get("number", int(last_receipt.number) + 1 if last_receipt is not None else 1))

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
        # Если это чек возврата, то мы обновляем чек продажи reason_id равен id чека возврата и reasonCheckName равен номеру чека возврата
        if data.get("type_operation") == 2:
            query_params = {
                "owner_id": data.get('owner_id'),
                "organization_id": data.get('organization_id'),
                "store_id": data.get('store_id'),
                "cash_shift_id": data.get('cash_shift_id'),
                "workplace_id": data.get('workplace_id'),
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
            filter_by, {**data}
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
        if len(receipt) == 0: return None

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
        from cash_shift.dao import CheckoutShiftDAO as CashShiftDAO

        logger = logging.getLogger(__name__)
        receipt = await cls.get_one_receipt(filter_by)

        if not receipt:
            logger.error("Receipt not found")
            return None

        # Получаем последнюю открытую смены через запрос получения послед смены,
        # в запрос передаем owner,organization and workplace
        cash_shift: CashShiftWithReceiptsResponse | None = await CashShiftDAO.get_last_checkout_shift(
            {
                "owner_id": filter_by.get('owner_id'),
                "organization_id": filter_by.get('organization_id'),
                "workplace_id": filter_by.get('workplace_id'),
                "closed": False,
            },
        )

        # Сравниваем ид кассовой смены в чеке и ид последней кассовой смены полученной через запрос,
        # если эти ид не равны значит чек ьыл отложенным, а если он был отложенным,
        # то мы ему перезаписываем ид кассовой смены на текущий
        # if receipt.__dict__.get("cash_shift_id") != cash_shift.id:
        #     print(1111111111111111111111111111111)

        receipts: list[Receipt] = await cls.update(
            filter_by,
            {
                "check_status": ReceiptStatus.CLOSED.value,
                "date": datetime.datetime.utcnow(),
                "cash_shift_id": cash_shift.id if receipt.__dict__.get("cash_shift_id") != cash_shift.id else receipt.__dict__.get("cash_shift_id")
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
