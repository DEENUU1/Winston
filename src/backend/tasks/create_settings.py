from config.database import get_db
from repositories.settings_repository import SettingsRepository
from schemas.settings_schema import SettingsInputSchema


def create_settings() -> None:
    print("Creating settings...")

    db = next(get_db())

    settings_repository = SettingsRepository(db)
    settings_input = SettingsInputSchema(agent_id=1)

    if not settings_repository.settings_exists_by_id(1):
        settings_repository.create_settings(settings_input)

    print("Creating settings done!")
