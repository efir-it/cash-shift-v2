from check_status.models import CheckStatus
from dao.base import BaseDAO


class CheckStatusDAO(BaseDAO):
    model = CheckStatus

    @classmethod
    async def json_find_by_id(cls, id):
        check_status = await cls.find_by_id(id)
        return {"id": check_status.id, "name": check_status.name}

    @classmethod
    async def json_get_all(cls, **filter_by):
        check_statuses = await cls.get_all()
        return [
            {"id": check_status.id, "name": check_status.name}
            for check_status in check_statuses
        ]
