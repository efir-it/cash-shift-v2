from pydantic import BaseModel


class CashShiftSchemas(BaseModel):
    id: int
    name: str
    store_id: int

    class Config:
        orm_mode = True
