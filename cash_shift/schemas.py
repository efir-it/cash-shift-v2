from pydantic import BaseModel
from datetime import datetime


class CashShiftSchemas(BaseModel):
    id: int
    date: str
    organization_id: int
    client_id: int
    rmk_id: int
    worker_id: int
    device_id: int
    status: bool

    class Config:
        orm_mode = True
