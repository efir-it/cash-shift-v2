from sqlalchemy import update
from cash_shift.models import CashShift
from dao.base import BaseDAO
from database import async_session_maker

class CashShiftDAO(BaseDAO):
    model = CashShift

    @classmethod
    async def hide_by_rmk_id(cls, rmk_id: int) -> dict:
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.rmk_id == rmk_id)
                .values(
                    {
                        "hide": True
                    }
                )
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.first()[0].__dict__
    
    async def hide_by_organization_id(cls, organization_id: int) -> dict:
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.organization_id == organization_id)
                .values(
                    {
                        "hide": True
                    }
                )
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.first()[0].__dict__ 
    
    async def hide_by_store_id(cls, store_id: int) -> dict:
    #     async with async_session_maker() as session:
    #         query = (
    #             update(cls.model)
    #             .where(cls.model.store_id == store_id)
    #             .values(
    #                 {
    #                     "hide": True
    #                 }
    #             )
    #             .returning(cls.model)
    #         )
    #         result = await session.execute(query)
    #         await session.commit()
    #         return result.first()[0].__dict__
        pass