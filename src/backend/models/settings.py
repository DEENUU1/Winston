from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    agent_id = Column(Integer, ForeignKey('agents.id'), unique=True, nullable=True)
    agent = relationship("Agent", back_populates="settings")
