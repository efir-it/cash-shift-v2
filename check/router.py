from fastapi import APIRouter

from check.dao import CheckDAO
from check.schemas import CheckSchema

router = APIRouter(prefix="/checks", tags=["Чеки"])


@router.get("")
async def get_checks() -> list[CheckSchema]:
    return await CheckDAO.get_all()


@router.get("/{id}")
async def get_check(id: int) -> CheckSchema:
    return await CheckDAO.find_by_id(id)


@router.post("")
async def add_check(contractor: dict):
    return await CheckDAO.add(**contractor)


@router.put("/{id}")
async def update_check(id: int, **data: dict):
    return await CheckDAO.update(id, **data)


@router.delete("/{id}")
async def delete_check(id: int):
    return await CheckDAO.delete(id)
