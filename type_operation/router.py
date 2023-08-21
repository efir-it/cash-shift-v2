from fastapi import APIRouter

from type_operation.dao import TypeOperationDAO
from type_operation.schemas import TypeOperationSchema

router = APIRouter(
    prefix='/type_operation',
    tags=['Тип устройства']
)


@router.get('')
async def get_type_operations() -> list[TypeOperationSchema]:
    return await TypeOperationDAO.get_all()


@router.get('/{id}')
async def get_type_operation(model_id: int) -> TypeOperationSchema:
    return await TypeOperationDAO.find_by_id(model_id)


@router.post('')
async def add_type_operation(contractor: dict):
    return await TypeOperationDAO.add(**contractor)


@router.put('')
async def update_type_operation(model_id: int, **data: dict):
    return await TypeOperationDAO.update(model_id, **data)


@router.delete('/')
async def delete_type_operation(model_id: int):
    return await TypeOperationDAO.delete(model_id)


