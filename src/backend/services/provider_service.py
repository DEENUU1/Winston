from sqlalchemy.orm import Session
from typing import List
from schemas.provider_schema import ProviderInputSchema, ProviderOutputSchema, ProviderUpdateApiKeySchema
from repositories.provider_repository import ProviderRepository
from fastapi.exceptions import HTTPException


class ProviderService:
    def __init__(self, session: Session):
        self.provider_repository = ProviderRepository(session)

    def create_provider(self, data: ProviderInputSchema) -> ProviderOutputSchema:
        if self.provider_repository.provider_exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="Provider already exists")

        return self.provider_repository.create_provider(data)

    def get_provider_details(self, _id: int) -> ProviderOutputSchema:
        if not self.provider_repository.provider_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Provider not found")

        return self.provider_repository.get_provider_details_by_id(_id)

    def update_provider_api_key(self, _id: int, data: ProviderUpdateApiKeySchema) -> ProviderOutputSchema:
        if not self.provider_repository.provider_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Provider not found")

        provider = self.provider_repository.get_provider_object_by_id(_id)
        return self.provider_repository.update_provider_api_key(provider, data)

    def get_providers(self) -> List[ProviderOutputSchema]:
        return self.provider_repository.get_providers()
