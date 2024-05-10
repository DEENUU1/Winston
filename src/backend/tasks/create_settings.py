from config.database import get_db
from schemas.settings_schema import SettingsInputSchema
from services.settings_service import SettingsService


def create_settings() -> None:
    print("Creating settings...")

    db = next(get_db())

    settings_service = SettingsService(db)
    settings_input = SettingsInputSchema(agent_id=1)
    settings_service.create_settings(settings_input)

    print("Creating settings done!")
