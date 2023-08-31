from sqlalchemy import select
from position_check.models import PositionCheck
from dao.base import BaseDAO
from database import async_session_maker


class PositionCheckDAO(BaseDAO):
    model = PositionCheck

    @classmethod
    async def json_find_by_id(cls, id):
        position_check = await cls.find_by_id(id)
        return {
            "id": position_check.id,
            "productID": position_check.product_id,
            "count": position_check.count,
            "price": position_check.price,
            "positionNum": position_check.position,
        }

    @classmethod
    async def json_get_all(cls, **filter_by):
        positions_check = await cls.get_all(**filter_by)
        return [
            {
                "id": position_check.id,
                "productID": position_check.product_id,
                "count": position_check.count,
                "price": position_check.price,
                "positionNum": position_check.position,
            }
            for position_check in positions_check
        ]
