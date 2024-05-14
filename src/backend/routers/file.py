from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from config.database import get_db
from services.file_service import FileService

router = APIRouter(
    prefix="/file",
    tags=["File"],
)


@router.post("/chat/{session_id}/")
def upload_file(
        session_id: str,
        background_task: BackgroundTasks,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    return FileService(db).create_file(session_id, file, background_task)


@router.get("/chat/{session_id}/")
def get_files(session_id: str, db: Session = Depends(get_db)):
    return FileService(db).get_files_by_session_id(session_id)


@router.get("/{_id}")
def get_file(_id: int, db: Session = Depends(get_db)):
    return FileService(db).get_file_details_by_id(_id)
