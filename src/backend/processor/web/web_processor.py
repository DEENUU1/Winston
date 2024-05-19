from .web_reader import WebReader
from ai.data_loader import split_files
from ai.rag import save_to_pinecone


def process_web_page(url: str) -> str:
    web_reader = WebReader()
    processed_file = web_reader.convert_html_to_pdf(url)

    documents = split_files(processed_file)

    for document in documents:
        file_metadata = f"{document.metadata.get('source')}:{document.metadata.get('page')}"

        document.metadata["file_source_page"] = file_metadata
        document.metadata["url"] = url
    save_to_pinecone(documents)

    return url
