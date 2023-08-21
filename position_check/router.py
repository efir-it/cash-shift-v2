from fastapi import APIRouter

from position_check.dao import PositionCheckDAO
from position_check.schemas import PositionCheckSchema

router = APIRouter(
    prefix='/position_check',
    tags=['Позиция чека']
)


@router.get('')
async def get_position_checks() -> list[PositionCheckSchema]:
    return await PositionCheckDAO.get_all()


@router.get('/{id}')
async def get_position_check(model_id: int) -> PositionCheckSchema:
    return await PositionCheckDAO.find_by_id(model_id)


@router.post('')
async def add_position_check(contractor: dict):
    return await PositionCheckDAO.add(**contractor)


@router.put('')
async def update_position_check(model_id: int, **data: dict):
    return await PositionCheckDAO.update(model_id, **data)


@router.delete('/')
async def delete_position_check(model_id: int):
    return await PositionCheckDAO.delete(model_id)


