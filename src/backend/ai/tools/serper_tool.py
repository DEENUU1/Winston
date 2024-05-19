from langchain.agents import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from config.settings import settings


def get_serper_tool() -> Tool:
    search = GoogleSerperAPIWrapper(serper_api_key=settings.SERPER_API_KEY)
    return Tool(
        name="google_search",
        func=search.run,
        description="useful for when you need to ask with search",
    )
