from pydantic import BaseModel


class FileInput(BaseModel):
    name: str
    path: str
    message_store_session_id: str


class FileOutput(BaseModel):
    id: int
    name: str
    path: str
    message_store_session_id: str

    class Config:
        orm_mode = True
        from_attributes = True
