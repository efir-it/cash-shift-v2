from pydantic import BaseModel
from datetime import datetime


class CheckSchema(BaseModel):
    id: int
    client_id: int
    date: datetime
    number: str
    amount: int
    number_fiscal_document: str
    cash_shift_id: int
    type_operation_id: int
    type_payment_id: int
    check_status_id: int
    type_taxation_id: int

    class Config:
        orm_mode = True
