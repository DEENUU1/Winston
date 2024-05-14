from models.provider import Provider
from config.database import engine
from models.llm import LLM
from models.tool import Tool
from models.agent import Agent
from models.settings import Settings
from models.snippet import Snippet
from models.file import File
from models.message import Message


def create_tables():
    Message.metadata.create_all(bind=engine)
    Provider.metadata.create_all(bind=engine)
    Agent.metadata.create_all(bind=engine)
    LLM.metadata.create_all(bind=engine)
    Tool.metadata.create_all(bind=engine)
    Settings.metadata.create_all(bind=engine)
    Snippet.metadata.create_all(bind=engine)
    File.metadata.create_all(bind=engine)
