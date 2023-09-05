from pydantic import BaseModel


class CheckStatusSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
