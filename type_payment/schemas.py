from pydantic import BaseModel


class TypePaymentSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


