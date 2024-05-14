from typing import List, Optional

from ai.tools.current_time import CurrentTimeTool
from schemas.agent_schema import AgentOutputSchema
from ai.tools.rag_tool import rag_tool


def get_tools(agent: AgentOutputSchema, llm) -> List:
    tools = [CurrentTimeTool(), rag_tool(llm)]

    # for tool in agent.tools:
    #     if tool.name == "current_time_tool":
    #         tools.append(CurrentTimeTool())
    #     if tool.name == "retriever_tool":
    #         tools.append(rag_tool(llm))

    return tools
