from sqlalchemy.orm import Session
from typing import List
from schemas.llm_schema import LLMInputSchema, LLMOutputSchema
from repositories.llm_repository import LLMRepository
from fastapi.exceptions import HTTPException


class LLMService:
    def __init__(self, session: Session):
        self.provider_repository = LLMRepository(session)

    def create_llm(self, data: LLMInputSchema) -> LLMOutputSchema:
        if self.provider_repository.llm_exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="LLM already exists")

        return self.provider_repository.create_llm(data)

    def get_llm_details(self, _id: int) -> LLMOutputSchema:
        if not self.provider_repository.llm_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="LLM not found")

        return self.provider_repository.get_llm_details(_id)

    def get_llms(self) -> List[LLMOutputSchema]:
        return self.provider_repository.get_llms()
