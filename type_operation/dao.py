from sqlalchemy import select
from type_operation.models import TypeOperation
from dao.base import BaseDAO
from database import async_session_maker


class TypeOperationDAO(BaseDAO):
    model = TypeOperation

    @classmethod
    async def json_find_by_id(cls, id):
        type_operation = await cls.find_by_id(id)
        return {"id": type_operation.id, "name": type_operation.name}

    @classmethod
    async def json_get_all(cls, **filter_by):
        types_operation = await cls.get_all()
        return [
            {"id": type_operation.id, "name": type_operation.name}
            for type_operation in types_operation
        ]
