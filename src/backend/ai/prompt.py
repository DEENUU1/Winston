from langchain_core.prompts import ChatPromptTemplate

from schemas.agent_schema import AgentOutputSchema


def get_base_prompt(agent: AgentOutputSchema) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"You are a helpful assistant. Your name is {agent.name}"
                f"This is your description {agent.description}."
                f"You have access to many different tools, use them if you need to.",
            ),
            ("placeholder", "{history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
