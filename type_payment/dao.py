from type_payment.models import TypePayment
from dao.base import BaseDAO


class TypePaymentDAO(BaseDAO):
    model = TypePayment

    @classmethod
    async def json_find_by_id(cls, id):
        type_payment = await cls.find_by_id(id)
        return {"id": type_payment.id, "name": type_payment.name}

    @classmethod
    async def json_get_all(cls, **filter_by):
        types_payment = await cls.get_all()
        return [
            {"id": type_payment.id, "name": type_payment.name}
            for type_payment in types_payment
        ]
