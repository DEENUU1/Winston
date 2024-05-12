from config.database import get_db
from repositories.snippet_repository import SnippetRepository
from schemas.snippet_schema import SnippetInputSchema


def create_snippets() -> None:
    print("Creating snippets...")

    db = next(get_db())

    snippet_repository = SnippetRepository(db)

    snippets = [
        SnippetInputSchema(
            name="Summary",
            prompt="Utilize advanced techniques to succinctly summarize the provided text, capturing key points and "
                   "central themes effectively."
        ),
        SnippetInputSchema(
            name="Text fix",
            prompt="Enhance text clarity, coherence, and eloquence through refined stylistic adjustments and "
                   "vocabulary enhancements, ensuring optimal readability and impact."
        ),
        SnippetInputSchema(
            name="Translate",
            prompt="Translate the text accurately while preserving its original meaning, nuance, and tone, "
                   "ensuring seamless communication across languages."
        ),
        SnippetInputSchema(
            name="Q&A",
            prompt="Generate insightful questions and comprehensive answers derived from the provided data, "
                   "facilitating deeper understanding and engagement with the content."
        ),
        SnippetInputSchema(
            name="Prompt optimizer",
            prompt="Optimize prompts for maximum effectiveness in guiding model responses, refining specificity, "
                   "clarity, and relevance to elicit desired outcomes efficiently."
        ),
    ]

    for snippet in snippets:
        if not snippet_repository.snippet_exists_by_name(snippet.name):
            created = snippet_repository.create_snippet(snippet)
            print(f"Created snippet: {created}")

    print("Creating snippets done!")
