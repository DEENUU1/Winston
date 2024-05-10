from typing import Type

from sqlalchemy.orm import Session

from models.settings import Settings
from schemas.settings_schema import SettingsInputSchema, SettingsOutputSchema, SettingsUpdateSchema


class SettingsRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_settings(self, data: SettingsInputSchema) -> SettingsOutputSchema:
        settings = Settings(**data.model_dump(exclude_none=True))
        self.session.add(settings)
        self.session.commit()
        self.session.refresh(settings)
        return SettingsOutputSchema.from_orm(settings)

    def settings_exists_by_id(self, _id: int) -> bool:
        return self.session.query(Settings).filter_by(id=_id).first() is not None

    def get_settings_detail_by_id(self, _id: int) -> SettingsOutputSchema:
        return SettingsOutputSchema.from_orm(self.session.query(Settings).filter_by(id=_id).first())

    def get_settings_object_by_id(self, _id: int) -> Type[Settings]:
        return self.session.query(Settings).filter_by(id=_id).first()

    def update_settings(self, settings: Type[Settings], data: SettingsUpdateSchema) -> SettingsOutputSchema:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(settings, key, value)
        self.session.commit()
        self.session.refresh(settings)
        return SettingsOutputSchema.from_orm(settings)
