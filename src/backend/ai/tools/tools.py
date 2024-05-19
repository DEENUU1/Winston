from typing import List, Optional

from ai.tools.rag_tool import rag_tool
from schemas.agent_schema import AgentOutputSchema
from ai.tools.web_reader_tool import WebReaderTool
from ai.tools.serper_tool import get_serper_tool
from ai.tools.weather_tool import get_weather_tool
from ai.tools.youtube_tool import YoutubeTool


def get_tools(agent: AgentOutputSchema, llm, session_id: Optional[str] = None) -> List:
    tools = [
        rag_tool(session_id),
        WebReaderTool(),
        YoutubeTool(),
        get_serper_tool(),
        get_weather_tool()
    ]

    # for tool in agent.tools:
    #     if tool.name == "current_time_tool":
    #         tools.append(CurrentTimeTool())
    #     if tool.name == "retriever_tool":
    #         tools.append(rag_tool(llm))

    return tools
