# from langchain_openai import ChatOpenAI
import datetime
import os
from typing import Union, Dict, Tuple

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langchain_groq import ChatGroq

from .memory import setup_memory
from .rag import get_retriever_tool


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class CurrentTimeTool(BaseTool):
    name = "current_time_tool"
    description = "Useful for when you need to answer questions about current date and time"

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}

    def _run(self) -> str:
        return get_current_time()

    async def _arun(self) -> str:
        raise NotImplementedError("custom_search does not support async")


load_dotenv()

# llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"))

retriever_tool = get_retriever_tool(llm)
tools = [CurrentTimeTool(), retriever_tool]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.",
        ),
        ("placeholder", "{history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm, tools, prompt)


def setup_agent(session_id):
    memory = setup_memory(session_id=session_id)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)
    return agent_executor
