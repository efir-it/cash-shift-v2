import datetime
from typing import Optional

from cash_shift.models import CashShift
from cash_shift.schemas import CashShiftResponse, CashShiftWithReceiptsResponse
from cash_shift.utils import change_format
from check.dao import CheckDAO
from dao.base import BaseDAO


class CheckoutShiftDAO(BaseDAO):
    model = CashShift

    @classmethod
    async def hide_by(cls, filter_by: dict = {}) -> None:
        await cls.update(filter_by=filter_by, data={"hide": True})

    @classmethod
    async def get_one_checkout_shift(
        cls, filter_by: dict = {}
    ) -> Optional[CashShiftWithReceiptsResponse]:
        checkout_shift: CashShift | None = await cls.get_one_or_none(filter_by)

        return (
            CashShiftWithReceiptsResponse(
                **checkout_shift.__dict__,
                receipts=await CheckDAO.get_all_receipts(
                    {"cash_shift_id": checkout_shift.id}
                )
            )
            if checkout_shift is not None
            else None
        )

    @classmethod
    async def get_last_checkout_shift(
        cls, filter_by: dict = {}
    ) -> Optional[CashShiftWithReceiptsResponse]:
        checkout_shifts: list[CashShift] | None = await cls.get_all(filter_by)
        checkout_shifts.sort(key=lambda cash_shift: cash_shift.date, reverse=True)
        checkout_shift = checkout_shifts[0] if len(checkout_shifts) > 0 else None

        return (
            CashShiftWithReceiptsResponse(
                **checkout_shift.__dict__,
                receipts=await CheckDAO.get_all_receipts(
                    {"cash_shift_id": checkout_shift.id}
                )
            )
            if checkout_shift is not None
            else None
        )

    @classmethod
    async def get_all_checkout_shifts(
        cls, filter_by: dict = {}
    ) -> list[CashShiftResponse]:
        checkout_shifts: list[CashShift] = await cls.get_all(filter_by)

        return [
            CashShiftResponse(**checkout_shift.__dict__)
            for checkout_shift in checkout_shifts
        ]

    @classmethod
    async def create_checkout_shift(
        cls, data: dict = {}
    ) -> Optional[CashShiftWithReceiptsResponse]:
        checkout_shift: CashShift = await cls.add(
            {**data, "date": datetime.datetime.utcnow()}
        )

        return (
            CashShiftWithReceiptsResponse(**checkout_shift.__dict__, receipts=[])
            if checkout_shift is not None
            else None
        )

    @classmethod
    async def update_checkout_shift(
        cls, filter_by: dict = {}, data: dict = {}
    ) -> Optional[CashShiftWithReceiptsResponse]:
        checkout_shifts: list[CashShift] = await cls.update(filter_by, data)

        return (
            CashShiftWithReceiptsResponse(
                **checkout_shifts[0].__dict__,
                receipts=await CheckDAO.get_all_receipts(
                    {"cash_shift_id": checkout_shifts[0].id}
                )
            )
            if len(checkout_shifts) > 0
            else None
        )
