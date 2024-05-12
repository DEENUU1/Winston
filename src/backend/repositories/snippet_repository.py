from typing import List, Type

from sqlalchemy.orm import Session

from models.snippet import Snippet
from schemas.snippet_schema import SnippetInputSchema, SnippetOutputSchema, SnippetUpdateSchema


class SnippetRepository:
    def __init__(self, session: Session):
        self.session = session

    def snippet_exists_by_name(self, name: str) -> bool:
        return self.session.query(Snippet).filter_by(name=name).first() is not None

    def snippet_exists_by_id(self, _id: int) -> bool:
        return self.session.query(Snippet).filter_by(id=_id).first() is not None

    def create_snippet(self, data: SnippetInputSchema) -> SnippetOutputSchema:
        provider = Snippet(**data.model_dump(exclude_none=True))
        self.session.add(provider)
        self.session.commit()
        self.session.refresh(provider)
        return SnippetOutputSchema.from_orm(provider)

    def get_snippet_details_by_id(self, _id: int) -> SnippetOutputSchema:
        return SnippetOutputSchema.from_orm(self.session.query(Snippet).filter_by(id=_id).first())

    def get_snippet_object_by_id(self, _id: int) -> Type[Snippet]:
        return self.session.query(Snippet).filter_by(id=_id).first()

    def get_snippet_object_by_name(self, name: str) -> Type[Snippet]:
        return self.session.query(Snippet).filter_by(name=name).first()

    def get_snippets(self) -> List[SnippetOutputSchema]:
        return [SnippetOutputSchema.from_orm(provider) for provider in self.session.query(Snippet).all()]

    def update_snippet(self, agent: Type[Snippet], data: SnippetUpdateSchema) -> SnippetOutputSchema:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(agent, key, value)
        self.session.commit()
        self.session.refresh(agent)
        return SnippetOutputSchema.from_orm(agent)

    def delete_snippet(self, agent: Type[Snippet]) -> None:
        self.session.delete(agent)
        self.session.commit()
        return


