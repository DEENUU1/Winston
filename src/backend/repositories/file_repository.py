from typing import List

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

    def get_files_by_session_id(self, session_id: str) -> List[FileOutput]:
        return [FileOutput.from_orm(file) for file in self.session.query(File).filter_by(session_id=session_id).all()]

    def get_file_details_by_id(self, _id: int) -> FileOutput:
        return FileOutput.from_orm(self.session.query(File).filter_by(id=_id).first())

    def file_exists_by_id(self, _id: int) -> bool:
        return self.session.query(File).filter_by(id=_id).first() is not None
