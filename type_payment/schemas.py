from pydantic import BaseModel


class TypePaymentSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
