from fastapi import APIRouter

from type_taxation.dao import TypeTaxationDAO
from type_taxation.schemas import TypeTaxationSchema

router = APIRouter(
    prefix='/type_taxation',
    tags=['Типы налогообложения']
)


@router.get('')
async def get_type_taxations() -> list[TypeTaxationSchema]:
    return await TypeTaxationDAO.get_all()


@router.get('/{id}')
async def get_type_taxation(model_id: int) -> TypeTaxationSchema:
    return await TypeTaxationDAO.find_by_id(model_id)


@router.post('')
async def add_type_taxation(contractor: dict):
    return await TypeTaxationDAO.add(**contractor)


@router.put('')
async def update_type_taxation(model_id: int, **data: dict):
    return await TypeTaxationDAO.update(model_id, **data)


@router.delete('/')
async def delete_type_taxation(model_id: int):
    return await TypeTaxationDAO.delete(model_id)


