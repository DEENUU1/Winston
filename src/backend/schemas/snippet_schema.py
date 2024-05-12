from pydantic import BaseModel


class SnippetInputSchema(BaseModel):
    name: str
    prompt: str


class SnippetOutputSchema(BaseModel):
    id: int
    name: str
    prompt: str

    class Config:
        orm_mode = True
        from_attributes = True


class SnippetUpdateSchema(BaseModel):
    name: str
    prompt: str
