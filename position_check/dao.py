from sqlalchemy import select

from dao.base import BaseDAO
from database import async_session_maker
from position_check.models import PositionCheck
from position_check.utils import change_format


class PositionCheckDAO(BaseDAO):
    model = PositionCheck

    @classmethod
    async def json_find_by_id(cls, id):
        position_check = await cls.find_by_id(id)
        if position_check is None:
            return position_check
        return change_format(position_check.__dict__)

    @classmethod
    async def json_get_all(cls, filter_by):
        positions_check = await cls.get_all(filter_by)
        return {
            "positions_check": [
                change_format(position_check.__dict__)
                for position_check in positions_check
            ]
        }
