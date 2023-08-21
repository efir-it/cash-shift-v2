from fastapi import APIRouter

from type_payment.dao import TypePaymentDAO
from type_payment.schemas import TypePaymentSchema
router = APIRouter(
    prefix='/type_payment',
    tags=['Тип устройства']
)


@router.get('')
async def get_type_payments() -> list[TypePaymentSchema]:
    return await TypePaymentDAO.get_all()


@router.get('/{id}')
async def get_type_payment(model_id: int) -> TypePaymentSchema:
    return await TypePaymentDAO.find_by_id(model_id)


@router.post('')
async def add_type_payment(contractor: dict):
    return await TypePaymentDAO.add(**contractor)


@router.put('')
async def update_type_payment(model_id: int, **data: dict):
    return await TypePaymentDAO.update(model_id, **data)


@router.delete('/')
async def delete_type_payment(model_id: int):
    return await TypePaymentDAO.delete(model_id)


