from typing import List, Type

from sqlalchemy.orm import Session
from schemas.provider_schema import ProviderOutput, ProviderInput, ProviderUpdateApiKey
from models.provider import Provider


class ProviderRepository:
    def __init__(self, session: Session):
        self.session = session

    def provider_exists_by_name(self, name: str) -> bool:
        return self.session.query(Provider).filter(name=name).first() is not None

    def create_provider(self, data: ProviderInput) -> ProviderOutput:
        provider = Provider(**data.dict())
        self.session.add(provider)
        self.session.commit()
        self.session.refresh(provider)
        return ProviderOutput.from_orm(provider)

    def get_provider_details(self, _id: int) -> ProviderOutput:
        return ProviderOutput.from_orm(self.session.query(Provider).filter(id=_id).first())

    def get_provider_object(self, _id: int) -> Type[Provider]:
        return self.session.query(Provider).filter(id=_id).first()

    def update_provider_api_key(self, provider: Type[Provider], data: ProviderUpdateApiKey) -> ProviderOutput:
        provider.api_key = data.api_key
        self.session.commit()
        self.session.refresh(provider)
        return ProviderOutput.from_orm(provider)

    def get_providers(self) -> List[ProviderOutput]:
        return [ProviderOutput.from_orm(provider) for provider in self.session.query(Provider).all()]