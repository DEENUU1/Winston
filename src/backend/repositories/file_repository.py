from sqlalchemy.orm import Session
from schemas.file_schema import FileInput, FileOutput
from models.file import File


class FileRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_file(self, data: FileInput) -> FileOutput:
        file = File(**data.model_dump(exclude_none=True))
        self.session.add(file)
        self.session.commit()
        self.session.refresh(file)
        return FileOutput.from_orm(file)
