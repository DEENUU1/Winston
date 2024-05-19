from typing import List, Optional

from ai.tools.current_time import CurrentTimeTool
from ai.tools.rag_tool import rag_tool
from schemas.agent_schema import AgentOutputSchema
from ai.tools.web_reader_tool import WebReaderTool


def get_tools(agent: AgentOutputSchema, llm, session_id: Optional[str] = None) -> List:
    tools = [CurrentTimeTool(), rag_tool(session_id), WebReaderTool()]

    # for tool in agent.tools:
    #     if tool.name == "current_time_tool":
    #         tools.append(CurrentTimeTool())
    #     if tool.name == "retriever_tool":
    #         tools.append(rag_tool(llm))

    return tools
