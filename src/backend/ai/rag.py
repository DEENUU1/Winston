# from langchain.docstore.document import Document
# import json
# from langchain.tools.retriever import create_retriever_tool
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
# from langchain_community.document_loaders import TextLoader
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.tools import Tool

# loader = TextLoader("data.txt")
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_documents(documents)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
# db = Chroma.from_documents(texts, embeddings, persist_directory="./db")
# db.persist()


db2 = Chroma(persist_directory="./db", embedding_function=embeddings)
retriever = db2.as_retriever(search_type="similarity", search_kwargs={"k": 3})


# retriever_tool = create_retriever_tool(
#     retriever,
#     "personal_data_tool",
#     "Tool to get access to personal data"
# )

def get_retriever_tool(llm):
    retriever_tool = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    return Tool(
        name="retriever_tool",
        func=retriever_tool,
        description="Tool to get access to personal data for example what is my name",
    )
