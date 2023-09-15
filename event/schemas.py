from datetime import datetime
import uuid

from pydantic import BaseModel


class EventSchemas(BaseModel):
    id: uuid.UUID
    status: str
    queue: str
    message: str
    send_time: datetime

    class Config:
        from_attributes = True
