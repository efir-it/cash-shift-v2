from pydantic import BaseModel


class TypeTaxationSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
