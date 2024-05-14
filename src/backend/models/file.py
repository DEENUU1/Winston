from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from config.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    path = Column(String)
    message_store_session_id = Column(Text, ForeignKey('message_store.session_id'))

    message = relationship("Message", back_populates="files")
