from pydantic import BaseModel


class TypeTaxationSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
