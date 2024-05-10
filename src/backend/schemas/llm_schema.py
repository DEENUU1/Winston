from pydantic import BaseModel


class LLMInputSchema(BaseModel):
    name: str
    provider_id: int


class LLMOutputSchema(BaseModel):
    id: int
    name: str
    provider_id: int

    class Config:
        orm_mode = True
        from_attributes = True
