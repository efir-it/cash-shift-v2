from fastapi import APIRouter

from check.dao import CheckDAO
from check.schemas import CheckSchema

router = APIRouter(
    prefix='/check',
    tags=['Чек']
)


@router.get('')
async def get_checks() -> list[CheckSchema]:
    return await CheckDAO.get_all()


@router.get('/{id}')
async def get_check(model_id: int) -> CheckSchema:
    return await CheckDAO.find_by_id(model_id)


@router.post('')
async def add_check(contractor: dict):
    return await CheckDAO.add(**contractor)


@router.put('')
async def update_check(model_id: int, **data: dict):
    return await CheckDAO.update(model_id, **data)


@router.delete('/')
async def delete_check(model_id: int):
    return await CheckDAO.delete(model_id)


