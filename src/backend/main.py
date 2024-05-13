from langchain_core.documents import Document

from ai.rag import save_to_pinecone

data = """text here."""
doc = Document(page_content=data)
save_to_pinecone([doc])
