from pydantic import BaseModel
from typing import Optional


class ProviderInputSchema(BaseModel):
    name: str


class ProviderOutputSchema(BaseModel):
    id: int
    name: str
    api_key: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

