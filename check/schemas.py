import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    owner_id: uuid.UUID
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


class BaseCheckRequestSchema(BaseModel):
    ownerId: uuid.UUID
    organizationId: uuid.UUID


class GetChecksRequestSchema(BaseCheckRequestSchema):
    storeId: uuid.UUID | None = None
    cashShiftId: uuid.UUID | None = None
    timeStart: datetime | None = None
    timeEnd: datetime | None = None
    status: int | None = None
    count: int | None = None
