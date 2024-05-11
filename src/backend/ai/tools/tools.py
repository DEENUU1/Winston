from typing import List

from ai.rag import get_retriever_tool
from ai.tools.current_time import CurrentTimeTool
from schemas.agent_schema import AgentOutputSchema


def get_tools(agent: AgentOutputSchema, llm) -> List:
    tools = []

    for tool in agent.tools:
        if tool.name == "current_time_tool":
            tools.append(CurrentTimeTool())
        if tool.name == "retriever_tool":
            tools.append(get_retriever_tool(llm))

    return tools
