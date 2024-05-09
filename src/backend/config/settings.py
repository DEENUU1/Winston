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


settings = Settings()
