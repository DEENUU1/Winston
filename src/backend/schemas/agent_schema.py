from typing import Optional, List

from pydantic import BaseModel

from .llm_schema import LLMOutputSchema
from .tool_schema import ToolOutputSchema


class AgentInputSchema(BaseModel):
    name: str
    description: str
    temperature: Optional[float] = 0.0  # TODO add pydantic to validate value of temp
    avatar: Optional[str] = None
    prompt: Optional[str] = None
    llm_id: int


class AgentOutputSchema(BaseModel):
    id: int
    name: str
    description: str
    temperature: Optional[float] = 0.0
    avatar: Optional[str] = None
    prompt: Optional[str] = None
    llm: LLMOutputSchema
    tools: List[ToolOutputSchema] = []

    class Config:
        orm_mode = True
        from_attributes = True


class AgentUpdateSchema(BaseModel):
    name: str = None
    description: str = None
    temperature: Optional[float] = 0.0
    avatar: Optional[str] = None
    prompt: Optional[str] = None
    llm_id: int


class AgentUpdateToolsSchema(BaseModel):
    operation_type: str
    tool_id: int
