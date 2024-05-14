from typing import Optional

from langchain.chains import RetrievalQA
from langchain_core.tools import Tool

from ai.rag import get_pinecone


def rag_tool(llm, session_id: Optional[str] = None) -> Tool:
    if not session_id:
        pinecone = get_pinecone()
    else:
        pinecone = get_pinecone(session_id)

    rag = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=pinecone.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    )

    return Tool(
        name="retriever_tool",
        func=rag.run,
        description="Use this tool to answer user's question about personal data and previous information"
    )
