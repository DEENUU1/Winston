from config.database import get_db
from repositories.agent_repository import AgentRepository
from schemas.agent_schema import AgentInputSchema


def create_agents() -> None:
    print("Creating agents...")

    db = next(get_db())

    agent_repository = AgentRepository(db)

    agents = [
        AgentInputSchema(name="Winston", description="Main agent", temperature=0.4, llm_id=1)
    ]

    for agent in agents:
        if not agent_repository.agent_exists_by_name(agent.name):
            created = agent_repository.create_agent(agent)
            print(f"Created llm: {created}")

    print("Creating agents done!")
