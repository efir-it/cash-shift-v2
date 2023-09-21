import uuid

from pydantic import BaseModel, ConfigDict


class PositionCheckSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    count: int
    price: int
    position: int
    client_id: uuid.UUID
    check_id: uuid.UUID
