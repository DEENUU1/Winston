from pydantic import BaseModel


class ToolInput(BaseModel):
    name: str
    description: str


class ToolOutput(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
        from_attributes = True
