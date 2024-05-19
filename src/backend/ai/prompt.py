from langchain_core.prompts import ChatPromptTemplate

from schemas.agent_schema import AgentOutputSchema
from utils.current_time import get_current_time


def get_base_prompt(agent: AgentOutputSchema) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"You are a helpful assistant. Your name is {agent.name}"
                f"This is your description {agent.description}."
                f"You have access to many different tools, use them if you need to."
                f"Current time is: {get_current_time()}",
            ),
            ("placeholder", "{history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
