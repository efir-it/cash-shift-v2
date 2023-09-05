from datetime import datetime

from pydantic import BaseModel


class RmkSchemas(BaseModel):
    id: int
    status: str
    queue: str
    message: str
    send_time: datetime

    class Config:
        from_attributes = True
