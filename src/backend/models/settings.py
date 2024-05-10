from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .relationships import agent_tool_association, tool_llm_association
from config.database import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    agent_id = Column(Integer, ForeignKey('agents.id'), unique=True, nullable=True)
    agent = relationship("Agent", back_populates="settings")
