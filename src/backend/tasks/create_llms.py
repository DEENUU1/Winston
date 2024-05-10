from config.database import get_db
from repositories.provider_repository import ProviderRepository
from schemas.llm_schema import LLMInput
from repositories.llm_repository import LLMRepository


def create_llms() -> None:
    print("Creating llms...")

    db = next(get_db())

    provider_repository = ProviderRepository(db)
    llm_repository = LLMRepository(db)

    groq_provider = provider_repository.get_provider_object_by_name("Groq")
    llms = ["llama3-8b-8192", "llama3-70b-8192"]

    for llm in llms:
        if not llm_repository.llm_exists_by_name(llm):
            created = llm_repository.create_llm(LLMInput(name=llm, provider_id=groq_provider.id))
            print(f"Created llm: {created}")

    print("Creating llms done!")
