from pydantic import BaseModel
from typing import Optional


class ProviderInput(BaseModel):
    name: str


class ProviderOutput(BaseModel):
    id: int
    name: str
    api_key: Optional[str] = None

    class Config:
        orm_mode = True


class ProviderUpdateApiKey(BaseModel):
    api_key: Optional[str] = None

