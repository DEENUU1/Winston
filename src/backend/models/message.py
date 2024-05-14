from sqlalchemy import Column, Integer, Text, DateTime, func
from sqlalchemy.orm import relationship

from config.database import Base


class Message(Base):
    __tablename__ = "message_store"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Text)
    message = Column(Text, index=True)
    created_at = Column(DateTime, default=func.now())

    files = relationship("File", back_populates="message")
