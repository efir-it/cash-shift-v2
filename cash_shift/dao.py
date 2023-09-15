import datetime
from typing import Optional
from sqlalchemy import update
from cash_shift.models import CashShift
from cash_shift.utils import change_format
from dao.base import BaseDAO
from check.dao import CheckDAO
from database import async_session_maker


class CheckoutShiftDAO(BaseDAO):
    model = CashShift

    @classmethod
    async def hide_by_workplace_id(cls, workplace_id) -> None:
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.workplace_id == workplace_id)
                .values({"hide": True})
            )
            await session.execute(query)
            await session.commit()
        

    @classmethod
    async def hide_by_organization_id(cls, organization_id) -> None:
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.organization_id == organization_id)
                .values({"hide": True})
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def hide_by_store_id(cls, store_id) -> None:
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.store_id == store_id)
                .values({"hide": True})
                .returning(cls.model)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def json_find_by_id(cls, id) -> Optional[dict]:
        checkout_shift = await cls.find_by_id(id)
        if checkout_shift is None:
            return checkout_shift
        checkout_shift = checkout_shift.__dict__
        checks = await CheckDAO.json_get_all(**{"cash_shift_id": checkout_shift["id"]})
        checkout_shift["checks"] = checks["checks"]
        return change_format(checkout_shift)

    @classmethod
    async def json_get_all(cls, **filter_by) -> dict:
        checkout_shifts = await cls.get_all(**filter_by)
        return {
            "checkoutShifts": [
                change_format(checkout_shift.__dict__)
                for checkout_shift in checkout_shifts
            ]
        }

    @classmethod
    async def json_add(cls, **data) -> dict:
        checkout_shift = await cls.add(**data)
        if checkout_shift is None:
            return checkout_shift
        checkout_shift = checkout_shift.__dict__
        checkout_shift["checks"] = []
        return change_format(checkout_shift)
    
    @classmethod
    async def json_update(cls, id, **data) -> dict:
        checkout_shift = await cls.update(id, **data)
        if checkout_shift is None:
            return checkout_shift
        checkout_shift = checkout_shift.__dict__
        checks = await CheckDAO.json_get_all(**{"cash_shift_id": checkout_shift["id"]})
        checkout_shift["checks"] = checks["checks"]
        
        return change_format(checkout_shift)

    

    