import datetime
from fastapi import APIRouter

from cash_shift.dao import CashShiftDAO
from cash_shift.schemas import CashShiftSchemas

router = APIRouter(
    prefix='/cash_shifts',
    tags=['Кассовые смены']
)


@router.get('')
async def get_cash_shifts() -> list[CashShiftSchemas]:
    return await CashShiftDAO.get_all()


@router.get('/{id}')
async def get_cash_shift(id: int) -> CashShiftSchemas:
    return await CashShiftDAO.find_by_id(id)


@router.post('')
async def add_cash_shift(item: dict):
    format = "%Y-%m-%dT%H:%M:%S"
    if "date" in item:
        item["date"] = datetime.datetime.strptime(item["date"], format)
    return await CashShiftDAO.add(**item)


@router.put('/{id}')
async def update_cash_shift(id: int, **data: dict):
    return await CashShiftDAO.update(id, **data)


@router.delete('/{id}')
async def delete_cash_shift(id: int):
    return await CashShiftDAO.delete(id)


