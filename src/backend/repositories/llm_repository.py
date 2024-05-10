from typing import List, Type

from sqlalchemy.orm import Session
from schemas.llm_schema import LLMInputSchema, LLMOutputSchema
from models.llm import LLM


class LLMRepository:
    def __init__(self, session: Session):
        self.session = session

    def llm_exists_by_name(self, name: str) -> bool:
        return self.session.query(LLM).filter_by(name=name).first() is not None

    def llm_exists_by_id(self, _id: int) -> bool:
        return self.session.query(LLM).filter_by(id=_id).first() is not None

    def create_llm(self, data: LLMInputSchema) -> LLMOutputSchema:
        provider = LLM(**data.model_dump(exclude_none=True))
        self.session.add(provider)
        self.session.commit()
        self.session.refresh(provider)
        return LLMOutputSchema.from_orm(provider)

    def get_llm_details(self, _id: int) -> LLMOutputSchema:
        return LLMOutputSchema.from_orm(self.session.query(LLM).filter_by(id=_id).first())

    def get_llm_object_by_id(self, _id: int) -> Type[LLM]:
        return self.session.query(LLM).filter_by(id=_id).first()

    def get_llm_object_by_name(self, name: str) -> Type[LLM]:
        return self.session.query(LLM).filter_by(name=name).first()

    def get_llms(self) -> List[LLMOutputSchema]:
        return [LLMOutputSchema.from_orm(provider) for provider in self.session.query(LLM).all()]
