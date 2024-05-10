from sqlalchemy.orm import Session
from typing import List
from schemas.tool_schema import ToolOutputSchema, ToolInputSchema
from repositories.tool_repository import ToolRepository
from fastapi.exceptions import HTTPException


class ToolService:
    def __init__(self, session: Session):
        self.tool_repository = ToolRepository(session)

    def create_tool(self, data: ToolInputSchema):
        if self.tool_repository.tool_exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="Tool already exists")

        return self.tool_repository.create_tool(data)

    def get_tools(self) -> List[ToolOutputSchema]:
        return self.tool_repository.get_tools()

    def get_tool_details(self, _id: int) -> ToolOutputSchema:
        if not self.tool_repository.tool_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Tool not found")

        return self.tool_repository.get_tool_details_by_id(_id)
