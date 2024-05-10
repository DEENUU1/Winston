from sqlalchemy.orm import Session
from schemas.settings_schema import SettingsInputSchema, SettingsOutputSchema, SettingsUpdateSchema
from repositories.settings_repository import SettingsRepository
from fastapi.exceptions import HTTPException


class SettingsService:
    def __init__(self, session: Session):
        self.settings_repository = SettingsRepository(session)

    def create_settings(self, data: SettingsInputSchema) -> SettingsOutputSchema:
        if self.settings_repository.settings_exists_by_id(1):
            raise HTTPException(status_code=400, detail="Settings already exists")

        return self.settings_repository.create_settings(data)

    def get_settings_detail_by_id(self, _id: int) -> SettingsOutputSchema:
        return self.settings_repository.get_settings_detail_by_id(_id)

    def update_settings(self, _id: int, data: SettingsUpdateSchema) -> SettingsOutputSchema:
        if not self.settings_repository.settings_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Settings not found")

        settings = self.settings_repository.get_settings_object_by_id(_id)
        return self.settings_repository.update_settings(settings, data)
