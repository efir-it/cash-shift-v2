from pydantic import BaseModel


class TypeOperationSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


