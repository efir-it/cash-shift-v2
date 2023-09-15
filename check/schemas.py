import uuid
from pydantic import BaseModel
from datetime import datetime


class CheckSchema(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    date: datetime
    number: str
    amount: int
    number_fiscal_document: str
    cash_shift_id: uuid.UUID
    type_operation: str
    type_payment: str
    check_status: str
    type_taxation: str

    class Config:
        from_attributes = True
