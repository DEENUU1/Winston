from models.provider import Provider
from config.database import engine
from models.llm import LLM
from models.tool import Tool
from models.agent import Agent
from models.settings import Settings


def create_tables():
    Provider.metadata.create_all(bind=engine)
    Agent.metadata.create_all(bind=engine)
    LLM.metadata.create_all(bind=engine)
    Tool.metadata.create_all(bind=engine)
    Settings.metadata.create_all(bind=engine)
