from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory


def setup_memory(session_id: str) -> ConversationBufferMemory:
    chat_message_history = SQLChatMessageHistory(session_id=session_id, connection_string="sqlite:///sqlite.db")

    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        chat_memory=chat_message_history,
    )
    return memory
