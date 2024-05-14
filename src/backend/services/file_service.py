from sqlalchemy.orm import Session

from repositories.file_repository import FileRepository
from schemas.file_schema import FileInput, FileOutput


class FileService:
    def __init__(self, session: Session):
        self.file_repository = FileRepository(session)

    def create(self, data: FileInput) -> FileOutput:
        return self.file_repository.create_file(data)
