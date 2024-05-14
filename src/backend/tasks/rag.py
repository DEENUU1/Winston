from ai.data_loader import split_files
from ai.rag import save_to_pinecone


def rag_process(file_path: str, session_id: str):
    documents = split_files(file_path)

    for document in documents:
        file_metadata = f"{document.metadata.get('source')}:{document.metadata.get('page')}"

        document.metadata["file_source_page"] = file_metadata
        document.metadata["session_id"] = session_id

        save_to_pinecone([document])
