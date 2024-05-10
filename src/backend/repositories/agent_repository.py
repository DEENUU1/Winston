from typing import List, Type

from sqlalchemy.orm import Session

from models.tool import Tool
from schemas.agent_schema import AgentOutputSchema, AgentInputSchema, AgentUpdateSchema
from models.agent import Agent


class AgentRepository:
    def __init__(self, session: Session):
        self.session = session

    def agent_exists_by_name(self, name: str) -> bool:
        return self.session.query(Agent).filter_by(name=name).first() is not None

    def agent_exists_by_id(self, _id: int) -> bool:
        return self.session.query(Agent).filter_by(id=_id).first() is not None

    def create_agent(self, data: AgentInputSchema) -> AgentOutputSchema:
        provider = Agent(**data.model_dump(exclude_none=True))
        self.session.add(provider)
        self.session.commit()
        self.session.refresh(provider)
        return AgentOutputSchema.from_orm(provider)

    def get_agent_details_by_id(self, _id: int) -> AgentOutputSchema:
        return AgentOutputSchema.from_orm(self.session.query(Agent).filter_by(id=_id).first())

    def get_agent_object_by_id(self, _id: int) -> Type[Agent]:
        return self.session.query(Agent).filter_by(id=_id).first()

    def get_agent_object_by_name(self, name: str) -> Type[Agent]:
        return self.session.query(Agent).filter_by(name=name).first()

    def get_agents(self) -> List[AgentOutputSchema]:
        return [AgentOutputSchema.from_orm(provider) for provider in self.session.query(Agent).all()]

    def update_agent(self, agent: Type[Agent], data: AgentUpdateSchema) -> AgentOutputSchema:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(agent, key, value)
        self.session.commit()
        self.session.refresh(agent)
        return AgentOutputSchema.from_orm(agent)

    def add_tool_to_agent(self, agent: Type[Agent], tool: Type[Tool]) -> None:
        agent.tools.append(tool)
        self.session.commit()
        return

    def remove_tool_from_agent(self, agent: Type[Agent], tool: Type[Tool]) -> None:
        agent.tools.remove(tool)
        self.session.commit()
        return

    def delete_agent(self, agent: Type[Agent]) -> None:
        self.session.delete(agent)
        self.session.commit()
        return


