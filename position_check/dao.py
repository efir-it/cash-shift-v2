import uuid
from sqlalchemy import select

from dao.base import BaseDAO
from database import async_session_maker
from position_check.models import PositionCheck
from position_check.schemas import PositionResponse
from sqlalchemy import Delete, Insert, Select, Update, delete, insert, select, update

class PositionCheckDAO(BaseDAO):
    model = PositionCheck

    @classmethod
    async def get_one_position(cls, filter_by: dict = {}) -> PositionResponse:
        position: PositionCheck = await cls.get_one_or_none(filter_by)

        return PositionResponse(**position.__dict__) if position is not None else None

    @classmethod
    async def get_all_positions(cls, filter_by: dict = {}, ) -> list[PositionResponse]:
        positions: list[PositionCheck] = await cls.get_all(filter_by)

        return [PositionResponse(**position.__dict__) for position in positions]


    @classmethod
    async def get_all_positions_by_ids(cls, filter_by: list = [uuid.UUID], ) -> list[PositionResponse]:

       async with async_session_maker() as session:
            query: Select = select(cls.model).where(cls.model.check_id.in_(filter_by))
            result = await session.execute(query)
            return [row[0] for row in result.fetchall()]
        
       
