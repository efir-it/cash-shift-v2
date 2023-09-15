import uuid
from pydantic import BaseModel
from datetime import datetime


class CashShiftSchemas(BaseModel):
    id: uuid.UUID
    date: datetime
    organization_id: uuid.UUID
    client_id: uuid.UUID
    store_id: uuid.UUID
    workplace_id: uuid.UUID
    personal_id: uuid.UUID
    cash_registr_id: uuid.UUID
    closed: bool
    hide: bool

    class Config:
        from_attributes = True
