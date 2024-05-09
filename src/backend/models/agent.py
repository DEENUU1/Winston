from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from config.database import Base
from .relationships import agent_tool_association


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    temperature = Column(Float)
    avatar = Column(String)
    prompt = Column(String)

    tools = relationship("Tool", secondary=agent_tool_association, back_populates="agents")
    llm = relationship("LLM", uselist=False, back_populates="agent")
