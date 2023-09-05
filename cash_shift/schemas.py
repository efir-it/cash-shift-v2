from pydantic import BaseModel
from datetime import datetime


class CashShiftSchemas(BaseModel):
    id: int
    date: datetime
    organization_id: int
    client_id: int
    store_id: int
    workplace_id: int
    personal_id: int
    cash_registr_id: int
    status: bool
    hide: bool

    class Config:
        from_attributes = True
