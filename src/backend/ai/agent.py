from langchain.agents import AgentExecutor, create_tool_calling_agent
from ai.llm import get_llm
from .memory import setup_memory
from ai.tools.tools import get_tools
from ai.prompt import get_base_prompt
from services.agent_service import AgentService
from config.database import get_db
from services.settings_service import SettingsService


def setup_agent(session_id: str):
    db = next(get_db())

    settings = SettingsService(db).get_settings_detail_by_id(1)
    agent_object = AgentService(db).get_agent_details_by_id(settings.agent_id)

    memory = setup_memory(session_id=session_id)
    llm = get_llm(agent_object)
    tools = get_tools(agent_object, llm, session_id)
    base_prompt = get_base_prompt(agent_object)

    agent = create_tool_calling_agent(llm, tools, base_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        memory=memory
    )
    return agent_executor
