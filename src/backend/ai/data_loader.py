from typing import List

from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    # CSVLoader,
    # JSONLoader,
    # UnstructuredMarkdownLoader,
    TextLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DataLoaderFactory:
    @staticmethod
    def split_docs(file_path: str):
        if file_path.endswith(".pdf"):
            return PyPDFLoader(file_path)
        # elif file_path.endswith(".csv"):
        #     return CSVLoader(file_path)
        # elif file_path.endswith(".json"):
        #     return JSONLoader(file_path)
        # elif file_path.endswith(".md"):
        #     return UnstructuredMarkdownLoader(file_path)
        elif file_path.endswith(".txt"):
            return TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError("Invalid file type")


def split_files(file_path: str) -> List[Document]:
    """
    Split files into chunks
    """
    loader = DataLoaderFactory().split_docs(file_path=file_path)
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False
    )
    documents = text_splitter.split_documents(document)

    return documents
