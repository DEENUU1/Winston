from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.settings_schema import SettingsUpdateSchema
from services.settings_service import SettingsService

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.put("/{id}")
def update_settings(_id: int, data: SettingsUpdateSchema, db: Session = Depends(get_db)):
    return SettingsService(db).update_settings(_id, data)


@router.get("/{id}")
def get_settings_details(_id: int, db: Session = Depends(get_db)):
    return SettingsService(db).get_settings_detail_by_id(_id)
