from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .relationships import agent_tool_association, tool_llm_association
from config.database import Base


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    agents = relationship("Agent", secondary=agent_tool_association, back_populates="tools")
    llms = relationship("LLM", secondary=tool_llm_association, back_populates="tools")
