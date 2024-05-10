from pydantic import BaseModel


class SettingsInputSchema(BaseModel):
    agent_id: int


class SettingsOutputSchema(BaseModel):
    id: int
    agent_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class SettingsUpdateSchema(BaseModel):
    agent_id: int
