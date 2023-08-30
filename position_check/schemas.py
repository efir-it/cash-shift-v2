from pydantic import BaseModel


class PositionCheckSchema(BaseModel):
    id: int
    product_id: int
    count: int
    price: int
    position: int
    client_id: int
    check_id: int

    class Config:
        orm_mode = True
