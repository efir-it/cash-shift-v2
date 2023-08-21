from pydantic import BaseModel


class CheckSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


