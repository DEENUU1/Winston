from config.database import get_db
from repositories.provider_repository import ProviderRepository
from schemas.provider_schema import ProviderInputSchema


def create_providers() -> None:
    print("Creating providers...")

    db = next(get_db())

    provider_repository = ProviderRepository(db)

    providers = ["Groq", "OpenAI"]

    for provider in providers:
        if not provider_repository.provider_exists_by_name(provider):
            created = provider_repository.create_provider(ProviderInputSchema(name=provider))
            print(f"Created provider: {created}")

    print("Creating providers done!")
