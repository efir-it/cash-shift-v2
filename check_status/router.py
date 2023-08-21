from fastapi import APIRouter

from check_status.dao import CheckStatusDAO
from check_status.schemas import CheckStatusSchema

router = APIRouter(
    prefix='/check_status',
    tags=['Статус чека']
)


@router.get('')
async def get_check_status_all() -> list[CheckStatusSchema]:
    return await CheckStatusDAO.get_all()


@router.get('/{id}')
async def get_check_status(model_id: int) -> CheckStatusSchema:
    return await CheckStatusDAO.find_by_id(model_id)


@router.post('')
async def add_check_status(contractor: dict):
    return await CheckStatusDAO.add(**contractor)


@router.put('')
async def update_check_status(model_id: int, **data: dict):
    return await CheckStatusDAO.update(model_id, **data)


@router.delete('/')
async def delete_check_status(model_id: int):
    return await CheckStatusDAO.delete(model_id)


