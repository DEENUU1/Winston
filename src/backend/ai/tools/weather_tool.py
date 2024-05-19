from langchain.agents import Tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from config.settings import settings


def get_weather_tool() -> Tool:
    search = OpenWeatherMapAPIWrapper(openweathermap_api_key=settings.OPENWEATHER_API_KEY)
    return Tool(
        name="weather",
        func=search.run,
        description="Use when you need to answer question about weather",
    )
