from typing import List, Optional

from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.chat_message_histories.sql import DefaultMessageConverter, BaseMessageConverter
from langchain_core.messages import BaseMessage, AIMessage

from config.settings import settings
from models.message import Message


class CustomDefaultMessageConverter(DefaultMessageConverter):
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.model_class = Message


class CustomSQLChatMessageHistory(SQLChatMessageHistory):
    """
    This class override SQLChatMessageHistory class from Langchain library
    """

    def __init__(
            self,
            session_id: str,
            table_name: str = "message_store",
            session_id_field_name: str = "session_id",
            custom_message_converter: Optional[BaseMessageConverter] = None,
    ):
        connection_string = settings.SQLITE_CONNECTION_STRING
        custom_converter_instance = custom_message_converter or CustomDefaultMessageConverter(table_name)

        super().__init__(
            session_id=session_id,
            connection_string=connection_string,
            table_name=table_name,
            session_id_field_name=session_id_field_name,
            custom_message_converter=custom_converter_instance,
        )

    def search_conversations_by_content(self, query: str) -> List[str]:
        with self.Session() as session:
            result = (
                session.query(self.sql_model_class)
                .filter(self.sql_model_class.message.contains(f"{query}"))
                .all()
            )
            output = []

            for record in result:
                output.append(self.converter.from_sql_model(record))
            return output

    def unique_session_ids(self) -> List[str]:
        """
        Retrieve all unique session IDs from db
        """
        with self.Session() as session:
            result = (
                session.query(getattr(self.sql_model_class, self.session_id_field_name))
                .distinct()
                .all()
            )
            return [row[0] for row in result]

    def get_messages_by_session_id(self) -> List[BaseMessage]:
        """
        Retrieve messages for a specific session ID
        """
        with self.Session() as session:
            result = (
                session.query(self.sql_model_class)
                .filter(
                    getattr(self.sql_model_class, self.session_id_field_name)
                    == self.session_id
                )
                .order_by(self.sql_model_class.id.asc())
            )

            messages = []
            for record in result:
                messages.append(self.converter.from_sql_model(record))
            return messages

    def create_conversation(self) -> None:
        """
        Create Message object with generated session_id
        """

        # Because message field is required the content is an empty string and type is system
        # Later in conversation user input is a 'human' type and AI response is 'ai' type
        empty_message = BaseMessage(content="Hi, how can I help you?", type="ai")
        with self.Session() as session:
            empty_sql_model = self.converter.to_sql_model(empty_message, self.session_id)
            session.add(empty_sql_model)
            session.commit()

    def delete_conversation(self) -> None:
        """
        Delete all Message objects with specified session_id
        """

        with self.Session() as session:
            session.query(self.sql_model_class).filter(
                getattr(self.sql_model_class, self.session_id_field_name)
                == self.session_id
            ).delete()
            session.commit()


def get_all_conversations() -> List[Optional[str]]:
    """
    Get all conversations from db
    """
    result = []
    session_ids = CustomSQLChatMessageHistory(session_id="null").unique_session_ids()

    for session_id in session_ids:
        sql_message = CustomSQLChatMessageHistory(session_id=session_id)
        messages = sql_message.messages

        for message in messages:
            if hasattr(message, 'content'):
                content = message.content
                source = "AI" if isinstance(message, AIMessage) else "HUMAN"
                result.append(f"{source}: {content}")

    return result


def setup_memory(session_id: str) -> ConversationBufferMemory:
    chat_message_history = CustomSQLChatMessageHistory(session_id=session_id)

    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        chat_memory=chat_message_history,
    )
    return memory
