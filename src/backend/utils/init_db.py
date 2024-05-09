from models.provider import Provider
from config.database import engine


def create_tables():
    Provider.metadata.create_all(bind=engine)
