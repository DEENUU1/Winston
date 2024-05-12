from typing import List

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from repositories.snippet_repository import SnippetRepository
from schemas.snippet_schema import SnippetOutputSchema, SnippetUpdateSchema, SnippetInputSchema


class SnippetService:
    def __init__(self, session: Session):
        self.snippet_repository = SnippetRepository(session)

    def create_snippet(self, snippet: SnippetInputSchema) -> SnippetOutputSchema:
        if self.snippet_repository.snippet_exists_by_name(snippet.name):
            raise HTTPException(status_code=400, detail="Snippet with this name already exists")

        return self.snippet_repository.create_snippet(snippet)

    def get_snippet_details_by_id(self, _id: int) -> SnippetOutputSchema:
        if not self.snippet_repository.snippet_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Snippet not found")

        return self.snippet_repository.get_snippet_details_by_id(_id)

    def get_snippets(self) -> List[SnippetOutputSchema]:
        return self.snippet_repository.get_snippets()

    def update_snippet(self, _id: int, data: SnippetUpdateSchema) -> SnippetOutputSchema:
        if not self.snippet_repository.snippet_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Snippet not found")

        snippet = self.snippet_repository.get_snippet_object_by_id(_id)

        return self.snippet_repository.update_snippet(snippet, data)

    def delete_snippet(self, _id: int) -> None:
        if not self.snippet_repository.snippet_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Snippet not found")

        snippet = self.snippet_repository.get_snippet_object_by_id(_id)

        return self.snippet_repository.delete_snippet(snippet)
