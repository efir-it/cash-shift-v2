from type_taxation.models import TypeTaxation
from dao.base import BaseDAO


class TypeTaxationDAO(BaseDAO):
    model = TypeTaxation

    @classmethod
    async def json_find_by_id(cls, id):
        type_taxation = await cls.find_by_id(id)
        return {"id": type_taxation.id, "name": type_taxation.name}

    @classmethod
    async def json_get_all(cls, **filter_by):
        types_taxation = await cls.get_all()
        return [
            {"id": type_taxation.id, "name": type_taxation.name}
            for type_taxation in types_taxation
        ]
