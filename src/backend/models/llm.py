from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base


class LLM(Base):
    __tablename__ = "llms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    provider_id = Column(Integer, ForeignKey('providers.id'))

    provider = relationship("Provider", back_populates="llms")
