from typing import Any, List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.schema import Document
import json
import tiktoken


def remove_keys(data: Any, keys_to_remove: List[str]) -> Any:
    if isinstance(data, dict):
        return {k: remove_keys(v, keys_to_remove) for k, v in data.items() if k not in keys_to_remove}
    elif isinstance(data, list):
        return [remove_keys(item, keys_to_remove) for item in data]
    else:
        return data


def split_response_to_documents(api_response: List[dict], chunk_size: int = 1000) -> List[Optional[Document]]:
    # Initialize text splitter and tokenizer
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size,
        chunk_overlap=0,
    )
    tokenizer = tiktoken.get_encoding("cl100k_base")  # Choose appropriate model encoding

    documents = []
    current_chunk = []
    current_size = 0

    for item in api_response:
        item_str = json.dumps(item)
        item_tokens = tokenizer.encode(item_str)
        item_size = len(item_tokens)

        # Check if adding this item exceeds the chunk size
        if current_size + item_size > chunk_size:
            # If it does, finalize the current chunk and start a new one
            if current_chunk:
                context = "\n".join(current_chunk)
                documents.append(Document(page_content=context, metadata={"source": "local"}))

            current_chunk = [item_str]
            current_size = item_size
        else:
            # Otherwise, add the item to the current chunk
            current_chunk.append(item_str)
            current_size += item_size

    # Add the last chunk if it has any content
    if current_chunk:
        context = "\n".join(current_chunk)
        documents.append(Document(page_content=context, metadata={"source": "local"}))

    return documents


with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

api_response = data["response"]
processed_api_response = remove_keys(api_response, ["logo", "flag"])
# print(api_response)

documents = split_response_to_documents(processed_api_response, chunk_size=1000)
print(len(documents))
print(documents[0])
# for doc in documents:
#     print(doc.page_content)
