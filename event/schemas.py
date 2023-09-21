import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventSchemas(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    queue: str
    message: str
    send_time: datetime
