from fastapi import APIRouter

from cash_shift.dao import CashShiftDAO
from cash_shift.schemas import CashShiftSchemas

router = APIRouter(
    prefix='/cash_shift',
    tags=['Кассовые смены']
)


@router.get('')
async def get_cash_shifts() -> list[CashShiftSchemas]:
    return await CashShiftDAO.get_all()


@router.get('/{id}')
async def get_cash_shift(model_id: int) -> CashShiftSchemas:
    return await CashShiftDAO.find_by_id(model_id)


@router.post('')
async def add_cash_shift(item: dict):
    return await CashShiftDAO.add(**item)


@router.put('')
async def update_cash_shift(model_id: int, **data: dict):
    return await CashShiftDAO.update(model_id, **data)


@router.delete('/')
async def delete_cash_shift(model_id: int):
    return await CashShiftDAO.delete(model_id)
