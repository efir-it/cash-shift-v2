import datetime
from typing import Optional

from sqlalchemy import update

from cash_shift.models import CashShift
from cash_shift.utils import change_format
from check.dao import CheckDAO
from dao.base import BaseDAO
from database import async_session_maker


class CheckoutShiftDAO(BaseDAO):
    model = CashShift

    @classmethod
    async def hide_by(cls, filter_by: dict = {}) -> None:
        await cls.update(filter_by=filter_by, data={"hide": True})

    @classmethod
    async def json_find_one(cls, id, filter_by: dict = {}) -> Optional[dict]:
        checkout_shift = await cls.get_one_or_none({"id": id, **filter_by})

        return (
            change_format(
                {
                    **checkout_shift.__dict__,
                    "checks": (
                        await CheckDAO.json_get_all(
                            {"cash_shift_id": checkout_shift.id}
                        )
                    )["checks"],
                }
            )
            if checkout_shift is not None
            else None
        )

    @classmethod
    async def json_get_all(cls, filter_by: dict = {}) -> dict:
        checkout_shifts = await cls.get_all(filter_by)

        return (
            {
                "checkoutShifts": [
                    change_format(checkout_shift.__dict__)
                    for checkout_shift in checkout_shifts
                ]
            }
            if checkout_shifts is not None
            else None
        )

    @classmethod
    async def json_add(cls, data: dict = {}) -> Optional[dict]:
        checkout_shift = await cls.add(data)

        return (
            change_format(checkout_shift.__dict__)
            if checkout_shift is not None
            else None
        )

    @classmethod
    async def json_update(
        cls, id, filter_by: dict = {}, data: dict = {}
    ) -> Optional[dict]:
        checkout_shifts = await cls.update({"id": id, **filter_by}, data)
        checkout_shift = checkout_shifts[0] if len(checkout_shifts) > 0 else None

        return (
            change_format(
                {
                    **(checkout_shift.__dict__),
                    "checks": (
                        await CheckDAO.json_get_all(
                            {"cash_shift_id": checkout_shift.id}
                        )
                    )["checks"],
                }
            )
            if checkout_shift is not None
            else None
        )
