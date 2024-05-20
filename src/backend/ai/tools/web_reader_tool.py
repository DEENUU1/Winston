from typing import Type

from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from ai.rag import get_pinecone
from processor.web.web_processor import process_web_page


class URLInput(BaseModel):
    query: str = Field(description="The query provided by user to process and find on the given page")
    url: str = Field(description="The url provided by user to process")


class WebReaderTool(BaseTool):
    name = "read_web_page"
    description = "Useful when user provides a url address to web page"
    args_schema: Type[BaseModel] = URLInput

    def _run(self, query: str, url: str):
        pinecone = get_pinecone()
        retriever = pinecone.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 10,
                "filter": {
                    "url": url
                }
            }
        )
        docs = retriever.get_relevant_documents("")

        if len(docs) == 0:
            process_web_page(url)

        docs = retriever.get_relevant_documents("")

        content = ""
        for doc in docs:
            content += doc.page_content

        return content

    async def _arun(self) -> str:
        raise NotImplementedError("custom_search does not support async")
