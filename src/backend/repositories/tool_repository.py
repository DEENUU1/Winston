from typing import List, Type

from sqlalchemy.orm import Session
from schemas.tool_schema import ToolInput, ToolOutput
from models.tool import Tool


class ToolRepository:
    def __init__(self, session: Session):
        self.session = session

    def tool_exists_by_name(self, name: str) -> bool:
        return self.session.query(Tool).filter_by(name=name).first() is not None

    def tool_exists_by_id(self, _id: int) -> bool:
        return self.session.query(Tool).filter_by(id=_id).first() is not None

    def create_tool(self, data: ToolInput) -> ToolOutput:
        provider = Tool(**data.model_dump(exclude_none=True))
        self.session.add(provider)
        self.session.commit()
        self.session.refresh(provider)
        return ToolOutput.from_orm(provider)

    def get_tool_details_by_id(self, _id: int) -> ToolOutput:
        return ToolOutput.from_orm(self.session.query(Tool).filter_by(id=_id).first())

    def get_tool_object_by_id(self, _id: int) -> Type[Tool]:
        return self.session.query(Tool).filter_by(id=_id).first()

    def get_tool_object_by_name(self, name: str) -> Type[Tool]:
        return self.session.query(Tool).filter_by(name=name).first()

    def get_tools(self) -> List[ToolOutput]:
        return [ToolOutput.from_orm(provider) for provider in self.session.query(Tool).all()]
