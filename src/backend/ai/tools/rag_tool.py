from typing import Optional

from langchain.tools.retriever import create_retriever_tool

from ai.rag import get_pinecone


def rag_tool(session_id: Optional[str] = None):
    pinecone = get_pinecone()

    if session_id:
        retriever = pinecone.as_retriever(search_type="similarity", search_kwargs={"k": 3}, namespace=session_id)
    else:
        retriever = pinecone.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    retriever_tool = create_retriever_tool(
        retriever,
        "retriever_tool",
        "Search for information about personal data and thinks about you don't have knowledge.",
    )
    return retriever_tool
