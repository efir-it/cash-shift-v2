import uuid
from pydantic import BaseModel


class PositionCheckSchema(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    count: int
    price: int
    position: int
    client_id: uuid.UUID
    check_id: uuid.UUID

    class Config:
        from_attributes = True
