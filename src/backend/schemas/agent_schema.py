from pydantic import BaseModel
from typing import Optional, List
from .llm_schema import LLMOutput
from .tool_schema import ToolOutput


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
    llm: LLMOutput
    tools: List[ToolOutput] = []


