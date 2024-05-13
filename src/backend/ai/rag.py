import os
from typing import List

from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone

from config.settings import settings

os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY


def get_embedding_func() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_EMBEDDING_MODEL)


def save_to_pinecone(data: List[Document]):
    embedding_func = get_embedding_func()

    vector_db = Pinecone.from_documents(data, embedding_func, index_name=settings.PINECONE_INDEX)
    return vector_db


def get_pinecone() -> Pinecone:
    embedding_func = get_embedding_func()

    return Pinecone.from_existing_index(index_name=settings.PINECONE_INDEX, embedding=embedding_func)
