from fastapi import APIRouter

from check_status.dao import CheckStatusDAO
from check_status.schemas import CheckStatusSchema

router = APIRouter(prefix="/check_statuses", tags=["Статусы чека"])


@router.get("")
async def get_check_status_all() -> list[CheckStatusSchema]:
    return await CheckStatusDAO.get_all()


@router.get("/{id}")
async def get_check_status(id: int) -> CheckStatusSchema:
    return await CheckStatusDAO.find_by_id(id)


@router.post("")
async def add_check_status(contractor: dict):
    return await CheckStatusDAO.add(**contractor)


@router.put("/{id}")
async def update_check_status(id: int, **data: dict):
    return await CheckStatusDAO.update(id, **data)


@router.delete("/{id}")
async def delete_check_status(id: int):
    return await CheckStatusDAO.delete(id)
