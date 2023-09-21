import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    client_id: uuid.UUID
    worker_id: uuid.UUID
    date: datetime
    number: str
    amount: int
    number_fiscal_document: str
    cash_shift_id: uuid.UUID
    type_operation: str
    type_payment: str
    check_status: str
    type_taxation: str
    reason_id: str
