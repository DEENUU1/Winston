from pydantic import BaseModel


class LLMInput(BaseModel):
    name: str
    provider_id: int


class LLMOutput(BaseModel):
    id: int
    name: str
    provider_id: int

    class Config:
        orm_mode = True
        from_attributes = True
