from pydantic import BaseModel


class ToolInputSchema(BaseModel):
    name: str
    description: str


class ToolOutputSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
        from_attributes = True
