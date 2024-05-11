import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import List
from schemas.agent_schema import AgentOutputSchema, AgentInputSchema, AgentUpdateSchema
from repositories.tool_repository import ToolRepository
from repositories.agent_repository import AgentRepository
from fastapi.exceptions import HTTPException


class AgentService:
    def __init__(self, session: Session):
        self.agent_repository = AgentRepository(session)
        self.tool_repository = ToolRepository(session)

    def create_agent(self, data: AgentInputSchema) -> AgentOutputSchema:
        if self.agent_repository.agent_exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="Agent already exists")

        return self.agent_repository.create_agent(data)

    def update_agent_avatar(self, _id: int, file: UploadFile) -> AgentOutputSchema:
        if not self.agent_repository.agent_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Agent not found")

        agent = self.agent_repository.get_agent_object_by_id(_id)

        avatar_path = f"media/avatar/{file.filename}"

        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return self.agent_repository.update_avatar(agent, avatar_path)

    def get_agents(self) -> List[AgentOutputSchema]:
        return self.agent_repository.get_agents()

    def get_agent_details_by_id(self, _id: int) -> AgentOutputSchema:
        if not self.agent_repository.agent_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Agent not found")

        return self.agent_repository.get_agent_details_by_id(_id)

    def update_agent(self, _id: int, data: AgentUpdateSchema) -> AgentOutputSchema:
        if not self.agent_repository.agent_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Agent not found")

        if self.agent_repository.agent_exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="Agent already exists")

        agent = self.agent_repository.get_agent_object_by_id(_id)
        return self.agent_repository.update_agent(agent, data)

    def delete_agent(self, _id: int) -> None:
        if not self.agent_repository.agent_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Agent not found")

        agent = self.agent_repository.get_agent_object_by_id(_id)
        self.agent_repository.delete_agent(agent)
        return None

    def add_tool_to_agent(self, agent_id: int, tool_id: int) -> None:
        if not self.agent_repository.agent_exists_by_id(agent_id):
            raise HTTPException(status_code=404, detail="Agent not found")

        if not self.tool_repository.tool_exists_by_id(tool_id):
            raise HTTPException(status_code=404, detail="Tool not found")

        agent = self.agent_repository.get_agent_object_by_id(agent_id)
        tool = self.tool_repository.get_tool_object_by_id(tool_id)

        self.agent_repository.add_tool_to_agent(agent, tool)
        return None

    def remove_tool_from_agent(self, agent_id: int, tool_id: int) -> None:
        if not self.agent_repository.agent_exists_by_id(agent_id):
            raise HTTPException(status_code=404, detail="Agent not found")

        if not self.tool_repository.tool_exists_by_id(tool_id):
            raise HTTPException(status_code=404, detail="Tool not found")

        agent = self.agent_repository.get_agent_object_by_id(agent_id)
        tool = self.tool_repository.get_tool_object_by_id(tool_id)

        self.agent_repository.remove_tool_from_agent(agent, tool)
        return None
