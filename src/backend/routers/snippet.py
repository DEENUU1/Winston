from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.snippet_schema import SnippetInputSchema, SnippetUpdateSchema
from services.snippet_service import SnippetService

router = APIRouter(
    prefix="/snippet",
    tags=["Snippet"],
)


@router.get("/")
def get_snippets(db: Session = Depends(get_db)):
    return SnippetService(db).get_snippets()


@router.get("/{_id}")
def get_snippet_by_id(_id: int, db: Session = Depends(get_db)):
    return SnippetService(db).get_snippet_details_by_id(_id)


@router.post("/")
def create_snippet(data: SnippetInputSchema, db: Session = Depends(get_db)):
    return SnippetService(db).create_snippet(data)


@router.put("/{_id}")
def update_snippet(_id: int, data: SnippetUpdateSchema, db: Session = Depends(get_db)):
    return SnippetService(db).update_snippet(_id, data)


@router.delete("/{_id}")
def delete_snippet(_id: int, db: Session = Depends(get_db)):
    return SnippetService(db).delete_snippet(_id)
