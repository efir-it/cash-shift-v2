from pydantic import BaseModel


class JWTUser(BaseModel):
    role: str
    data: dict
