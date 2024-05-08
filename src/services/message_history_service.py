from typing import Optional

from ai.memory import CustomSQLChatMessageHistory, get_all_conversations
from fastapi.exceptions import HTTPException


class MessageHistoryService:
    def __init__(self, session_id: str = "None"):
        self.session_id = session_id
        self.custom_sql_chat_message_history = CustomSQLChatMessageHistory(self.session_id)

    @staticmethod
    def get_all_conversations():
        return get_all_conversations()

    def search_conversations_by_content(self, query: str):
        return self.custom_sql_chat_message_history.search_conversations_by_content(query)

    def get_unique_session_ids(self):
        return self.custom_sql_chat_message_history.unique_session_ids()

    def get_messages_by_session_id(self):
        if self.session_id == "None":
            raise HTTPException(status_code=400, detail="Session id is required")

        return self.custom_sql_chat_message_history.get_messages_by_session_id()

    def create_conversation(self):
        if self.session_id == "None":
            raise HTTPException(status_code=400, detail="Session id is required")

        return self.custom_sql_chat_message_history.create_conversation()

    def delete_conversation(self):
        if self.session_id == "None":
            raise HTTPException(status_code=400, detail="Session id is required")

        return self.custom_sql_chat_message_history.delete_conversation()
