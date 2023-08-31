from fastapi import APIRouter

from type_operation.dao import TypeOperationDAO
from type_operation.schemas import TypeOperationSchema

router = APIRouter(prefix="/types_operation", tags=["Типы операции"])


# @router.get("")
# async def get_type_operations() -> list[TypeOperationSchema]:
#     return await TypeOperationDAO.get_all()


# @router.get("/{id}")
# async def get_type_operation(id: int) -> TypeOperationSchema:
#     return await TypeOperationDAO.find_by_id(id)


# @router.post("")
# async def add_type_operation(contractor: dict):
#     return await TypeOperationDAO.add(**contractor)


# @router.put("/{id}")
# async def update_type_operation(id: int, **data: dict):
#     return await TypeOperationDAO.update(id, **data)


# @router.delete("/{id}")
# async def delete_type_operation(id: int):
#     return await TypeOperationDAO.delete(id)

# @router.get("/json/{id}")
# async def get_json_type_operation(id: int):
#     return await TypeOperationDAO.json_find_by_id(id)

# @router.get("/json/")
# async def get_json_types_operation():
#     return await TypeOperationDAO.json_get_all()
