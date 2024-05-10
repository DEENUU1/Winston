from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from services.tool_service import ToolService

router = APIRouter(
    prefix="/tool",
    tags=["Tool"],
)


@router.get("/")
def get_tools(db: Session = Depends(get_db)):
    return ToolService(db).get_tools()
