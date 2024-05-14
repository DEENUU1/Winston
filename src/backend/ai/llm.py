from services.provider_service import ProviderService
from config.database import get_db
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from schemas.agent_schema import AgentOutputSchema


def get_llm(agent: AgentOutputSchema):
    db = next(get_db())

    provider = ProviderService(db).get_provider_details(agent.llm.provider_id)

    provider_name = provider.name

    if provider_name == "OpenAI":
        return ChatOpenAI(openai_api_key=provider.api_key, temperature=agent.temperature)

    elif provider_name == "Groq":
        return ChatGroq(groq_api_key=provider.api_key) #, temperature=agent.temperature)

    else:
        raise Exception("Provider not supported")

