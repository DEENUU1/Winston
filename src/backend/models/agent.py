from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base
from .relationships import agent_tool_association


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    temperature = Column(Float, default=0.0, nullable=False)
    avatar = Column(String, nullable=True)
    prompt = Column(String, nullable=True)
    llm_id = Column(Integer, ForeignKey('llms.id'))

    tools = relationship("Tool", secondary=agent_tool_association, back_populates="agents")
    llm = relationship("LLM", back_populates="agent")
