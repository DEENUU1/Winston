from typing import List, Type

from sqlalchemy.orm import Session
from schemas.llm_schema import LLMInput, LLMOutput
from models.llm import LLM


class LLMRepository:
    def __init__(self, session: Session):
        self.session = session

    def llm_exists_by_name(self, name: str) -> bool:
        return self.session.query(LLM).filter_by(name=name).first() is not None

    def create_llm(self, data: LLMInput) -> LLMOutput:
        provider = LLM(**data.model_dump(exclude_none=True))
        self.session.add(provider)
        self.session.commit()
        self.session.refresh(provider)
        return LLMOutput.from_orm(provider)

    def get_llm_details(self, _id: int) -> LLMOutput:
        return LLMOutput.from_orm(self.session.query(LLM).filter(id=_id).first())

    def get_llm_object(self, _id: int) -> Type[LLM]:
        return self.session.query(LLM).filter(id=_id).first()

    def get_llm(self) -> List[LLMOutput]:
        return [LLMOutput.from_orm(provider) for provider in self.session.query(LLM).all()]
