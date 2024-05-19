import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Application settings.
    """
    # Debug mode is set by default to True because it's local application
    DEBUG: bool = True
    # Title is the name of application
    TITLE: str = "Winston"
    # SQLITE connection string
    SQLITE_CONNECTION_STRING: Optional[str] = "sqlite:///sqlite.db"
    # Pinecone API key
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    # OpenAI API key
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    PINECONE_INDEX: Optional[str] = os.getenv("PINECONE_INDEX")
    OPENAI_EMBEDDING_MODEL: Optional[str] = os.getenv("OPENAI_EMBEDDING_MODEL")
    # Integrations
    SERPER_API_KEY: Optional[str] = os.getenv("SERPER_API_KEY")


settings = Settings()
