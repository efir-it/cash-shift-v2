import datetime
from sqlalchemy import update
from cash_shift.models import CashShift
from dao.base import BaseDAO
from check.dao import CheckDAO
from database import async_session_maker


class CheckoutShiftDAO(BaseDAO):
    model = CashShift

    @classmethod
    async def hide_by_rmk_id(cls, rmk_id: int) -> dict:
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.rmk_id == rmk_id)
                .values({"hide": True})
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.first()[0].__dict__

    @classmethod
    async def hide_by_organization_id(cls, organization_id: int) -> dict:
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.organization_id == organization_id)
                .values({"hide": True})
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.first()[0].__dict__

    @classmethod
    async def hide_by_store_id(cls, store_id: int) -> dict:
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.store_id == store_id)
                .values({"hide": True})
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.first()[0].__dict__

    @classmethod
    async def json_find_by_id(cls, id) -> dict:
        checkout_shift = await cls.find_by_id(id)
        return {
            "id": checkout_shift.id,
            "clientID": checkout_shift.client_id,
            "organizationID": checkout_shift.organization_id,
            "storeID": checkout_shift.store_id,
            "workplaceID": checkout_shift.workplace_id,
            "personalID": checkout_shift.personal_id,
            "cashRegistrID": checkout_shift.cash_registr_id,
            "passClosed": not checkout_shift.status,
            "passHidden": checkout_shift.hide,
            "openedTime": datetime.datetime.strftime(
                checkout_shift.date, "%Y-%m-%dT%H:%M:%S"
            ),
            "cashReceipts": await CheckDAO.json_get_all(
                **{"cash_shift_id": checkout_shift.id}
            ),
        }

    @classmethod
    async def json_update(cls, id, **data) -> dict:
        checkout_shift = await cls.update(id, **data)
        return {
            "id": checkout_shift.id,
            "openedTime": datetime.datetime.strftime(
                checkout_shift.date, "%Y-%m-%dT%H:%M:%S"
            ),
            "organizationID": checkout_shift.organization_id,
            "storeID": checkout_shift.store_id,
            "clientID": checkout_shift.client_id,
            "workplaceID": checkout_shift.workplace_id,
            "personalID": checkout_shift.personal_id,
            "cashRegistrID": checkout_shift.cash_registr_id,
            "passClosed": not checkout_shift.status,
            "passHidden": checkout_shift.hide,
            "cashReceipts": await CheckDAO.json_get_all(
                **{"cash_shift_id": checkout_shift.id}
            ),
        }

    @classmethod
    async def json_add(cls, **data) -> dict:
        data["status"] = True
        data["hide"] = False
        checkout_shift = await cls.add(**data)
        return {
            "id": checkout_shift.id,
            "openedTime": datetime.datetime.strftime(
                checkout_shift.date, "%Y-%m-%dT%H:%M:%S"
            ),
            "organizationID": checkout_shift.organization_id,
            "storeID": checkout_shift.store_id,
            "clientID": checkout_shift.client_id,
            "workplaceID": checkout_shift.workplace_id,
            "personalID": checkout_shift.personal_id,
            "cashRegistrID": checkout_shift.cash_registr_id,
            "passClosed": not checkout_shift.status,
            "passHidden": checkout_shift.hide,
            "cashReceipts": [],
        }

    @classmethod
    async def json_get_all(cls, **filter_by) -> dict:
        checkout_shifts = await cls.get_all(**filter_by)
        return [
            {
                "id": checkout_shift.id,
                "clientID": checkout_shift.client_id,
                "organizationID": checkout_shift.organization_id,
                "storeID": checkout_shift.store_id,
                "workplaceID": checkout_shift.workplace_id,
                "personalID": checkout_shift.personal_id,
                "cashRegistrID": checkout_shift.cash_registr_id,
                "passClosed": not checkout_shift.status,
                "passHidden": checkout_shift.hide,
                "openedTime": datetime.datetime.strftime(
                    checkout_shift.date, "%Y-%m-%dT%H:%M:%S"
                ),
                # "cashReceipts": await CheckDAO.json_get_all(
                #     **{"cash_shift_id": checkout_shift.id}
                # ),
            }
            for checkout_shift in checkout_shifts
        ]
