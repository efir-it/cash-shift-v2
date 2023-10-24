import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CashShiftSchemas(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    date: datetime
    organization_id: uuid.UUID
    owner_id: uuid.UUID
    store_id: uuid.UUID
    workplace_id: uuid.UUID
    worker_id: uuid.UUID
    cash_registr_id: uuid.UUID
    closed: bool
    hide: bool
