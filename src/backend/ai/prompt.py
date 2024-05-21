from langchain_core.prompts import PromptTemplate

from schemas.agent_schema import AgentOutputSchema
from utils.current_time import get_current_time


def get_base_prompt(agent: AgentOutputSchema) -> PromptTemplate:
    agent_prompt = f"""
        Current time is: {get_current_time()}
        Your name is {agent.name} and {agent.description}
    """

    prompt = """
        Answer the following questions as best you can. You have access to the following tools:
        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        history: {history}
        Question: {input}
        Thought:{agent_scratchpad}
    """

    full_prompt = agent_prompt + "\n" + prompt

    base_prompt = PromptTemplate(
        template=full_prompt,
        input_variables=["history", "input", "agent_scratchpad", "tools", "tool_names"]
    )
    return base_prompt
