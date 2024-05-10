from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from services.llm_service import LLMService


router = APIRouter(
    prefix="/llm",
    tags=["LLM"],
)


@router.get("/{id}")
def get_llm_details(id: int, db: Session = Depends(get_db)):
    return LLMService(db).get_llm_details(id)


@router.get("/")
def get_llms(db: Session = Depends(get_db)):
    return LLMService(db).get_llms()
