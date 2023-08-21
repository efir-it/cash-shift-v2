from type_payment.models import TypePayment
from dao.base import BaseDAO


class TypePaymentDAO(BaseDAO):
    model = TypePayment
