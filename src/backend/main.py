# from langchain_core.documents import Document
#
# from ai.rag import save_to_pinecone
#
# data = """text here."""
# doc = Document(page_content=data)
# save_to_pinecone([doc])
from langchain_openai import ChatOpenAI

from ai.tools.rag_tool import get_retriever

llm = ChatOpenAI(openai_api_key="sk-proj-XaZLnMS2RlrDcvw9uC8iT3BlbkFJJXPF4OcVwHNusaUJsa7W")

retriever = get_retriever(llm)

question = retriever({"query": "Jakie zadania na maturze wystąpiły w tym roku z matematyki? "})
print(question)