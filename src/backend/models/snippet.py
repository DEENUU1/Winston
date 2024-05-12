from sqlalchemy import Column, Integer, String

from config.database import Base


class Snippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    prompt = Column(String)
