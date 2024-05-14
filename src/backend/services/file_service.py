import os
import shutil
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from repositories.file_repository import FileRepository
from schemas.file_schema import FileInput, FileOutput
from services.message_history_service import MessageHistoryService


class FileService:
    def __init__(self, session: Session):
        self.file_repository = FileRepository(session)
        self.message_history_service = MessageHistoryService()

    def create_file(self, session_id: str, file: UploadFile) -> FileOutput:
        if not self.message_history_service.session_id_exists(session_id):
            raise HTTPException(status_code=404, detail="Session not found")

        file_extension = os.path.splitext(file.filename)[1]
        random_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"media/files/{random_filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_input = FileInput(name=file.filename, path=file_path, message_store_session_id=session_id)

        return self.file_repository.create_file(file_input)