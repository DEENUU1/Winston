from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base


class LLM(Base):
    __tablename__ = "llms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    provider_id = Column(Integer, ForeignKey('providers.id'))

    provider = relationship("Provider", back_populates="llms")
    agent_id = Column(Integer, ForeignKey('agents.id'))
    agent = relationship("Agent", back_populates="llm")
