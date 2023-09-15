import datetime
from typing import Optional
from check.models import Check
from dao.base import BaseDAO
from check.utils import CheckStatuses, change_format

from position_check.dao import PositionCheckDAO


class CheckDAO(BaseDAO):
    model = Check
    
    @classmethod
    async def get_check_with_positions(cls, check: dict, positions = None):
        if positions is None:
            positions = await PositionCheckDAO.json_get_all(**{"check_id": check["id"]})
        check["positions"] = positions["positions_check"]
        
        return check

    @classmethod
    async def json_find_by_id(cls, id) -> Optional[dict]:
        check = await cls.find_by_id(id)
        if check is None:
            return check
        check = await cls.get_check_with_positions(check.__dict__)
        
        return change_format(check)

    @classmethod
    async def json_get_all(cls, **filter_by) -> Optional[dict]:
        checks = await cls.get_all(**filter_by)
        
        return {
            "checks": [
                change_format(await cls.get_check_with_positions(check.__dict__))
                for check in checks
            ]
        }

    @classmethod
    async def json_add(cls, **data) -> Optional[dict]:
        positions_check = data.pop("positions", [])
        check = await cls.add(**data)
        for position, position_check in enumerate(positions_check):
            await PositionCheckDAO.add(
                **{
                    "product_id": position_check["productId"],
                    "count": position_check["count"],
                    "price": position_check["price"],
                    "client_id": check.client_id,
                    "check_id": check.id,
                    "position": position + 1,
                }
            )
        check = await cls.get_check_with_positions(check.__dict__)
        
        return change_format(check)

    @classmethod
    async def json_remove(cls, id) -> Optional[dict]:
        positions = await PositionCheckDAO.json_get_all(**{"check_id": id})
        check = await cls.delete(id)
        if check is None:
            return check
        check = await cls.get_check_with_positions(check.__dict__, positions)
        
        return change_format(check)

    @classmethod
    async def json_update(cls, id, **data) -> Optional[dict]:
        check = await cls.update(id, **data)
        if check is None:
            return check
        check = await cls.get_check_with_positions(check.__dict__)
        
        return change_format(check)
