from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from config.database import get_db
from services.file_service import FileService


router = APIRouter(
    prefix="/file",
    tags=["File"],
)


@router.post("/{session_id}/")
def upload_file(session_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return FileService(db).create_file(session_id, file)