from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from services.provider_service import ProviderService
from schemas.provider_schema import ProviderUpdateApiKeySchema


router = APIRouter(
    prefix="/provider",
    tags=["Provider"],
)


@router.get("/")
def get_providers(session: Session = Depends(get_db)):
    return ProviderService(session).get_providers()


@router.put("/{id}")
def update_provider(_id: int, data: ProviderUpdateApiKeySchema, session: Session = Depends(get_db)):
    return ProviderService(session).update_provider_api_key(_id, data)
