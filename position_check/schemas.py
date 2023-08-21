from pydantic import BaseModel


class PositionCheckSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


