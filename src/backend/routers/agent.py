from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.agent_schema import AgentUpdateSchema, AgentInputSchema, AgentUpdateToolsSchema
from services.agent_service import AgentService

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post("/")
def create_agent(data: AgentInputSchema, db: Session = Depends(get_db)):
    agent = AgentService(db).create_agent(data)
    return agent


@router.get("/")
def get_agents(db: Session = Depends(get_db)):
    return AgentService(db).get_agents()


@router.get("/{id}")
def get_agent_details_by_id(id: int, db: Session = Depends(get_db)):
    return AgentService(db).get_agent_details_by_id(id)


@router.put("/{id}")
def update_agent(id: int, data: AgentUpdateSchema, db: Session = Depends(get_db)):
    return AgentService(db).update_agent(id, data)


@router.delete("/{id}")
def delete_agent(id: int, db: Session = Depends(get_db)):
    return AgentService(db).delete_agent(id)


@router.put("/{id}/tool")
def add_tool_to_agent(id: int, data: AgentUpdateToolsSchema, db: Session = Depends(get_db)):
    if data.operation_type == "add":
        return AgentService(db).add_tool_to_agent(id, data.tool_id)
    elif data.operation_type == "remove":
        return AgentService(db).remove_tool_from_agent(id, data.tool_id)
    else:
        return {"message": "Invalid operation type"}
