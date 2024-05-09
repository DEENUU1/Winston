from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    api_key = Column(String)

    llms = relationship("LLM", back_populates="provider")
