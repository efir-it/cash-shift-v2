from fastapi import APIRouter

from position_check.dao import PositionCheckDAO
from position_check.schemas import PositionCheckSchema

router = APIRouter(prefix="/positions_check", tags=["Позиции чека"])


@router.get("")
async def get_position_checks() -> list[PositionCheckSchema]:
    return await PositionCheckDAO.get_all()


@router.get("/{id}")
async def get_position_check(id: int) -> PositionCheckSchema:
    return await PositionCheckDAO.find_by_id(id)


@router.post("")
async def add_position_check(contractor: dict):
    return await PositionCheckDAO.add(**contractor)


@router.put("/{id}")
async def update_position_check(id: int, **data: dict):
    return await PositionCheckDAO.update(id, **data)


@router.delete("/{id}")
async def delete_position_check(id: int):
    return await PositionCheckDAO.delete(id)
