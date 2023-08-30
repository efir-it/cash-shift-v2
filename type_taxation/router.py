from fastapi import APIRouter

from type_taxation.dao import TypeTaxationDAO
from type_taxation.schemas import TypeTaxationSchema

router = APIRouter(prefix="/type_taxation", tags=["Типы налогообложения"])


@router.get("")
async def get_type_taxations() -> list[TypeTaxationSchema]:
    return await TypeTaxationDAO.get_all()


@router.get("/{id}")
async def get_type_taxation(id: int) -> TypeTaxationSchema:
    return await TypeTaxationDAO.find_by_id(id)


@router.post("")
async def add_type_taxation(contractor: dict):
    return await TypeTaxationDAO.add(**contractor)


@router.put("/{id}")
async def update_type_taxation(id: int, **data: dict):
    return await TypeTaxationDAO.update(id, **data)


@router.delete("/{id}")
async def delete_type_taxation(id: int):
    return await TypeTaxationDAO.delete(id)
