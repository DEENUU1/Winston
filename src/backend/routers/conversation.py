from fastapi import APIRouter, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from ai.agent import setup_agent
from schemas.message import MessageInput
from services.message_history_service import MessageHistoryService
from utils.random_string import get_random_string

router = APIRouter(
    prefix="",
    tags=["Conversation"],
)


@router.post("/conversation/new/")
def create_conversation():
    random_string = get_random_string()
    MessageHistoryService(random_string).create_conversation()
    return JSONResponse(content={"session_id": random_string})

# @router.post("/conversation/search/")
# def search_conversations(
#         query: str = Form(...)
# ):
#     message_history_service = MessageHistoryService()
#     conversations = message_history_service.search_conversations_by_content(query)
#     return conversations


@router.post("/conversation/{session_id}")
def send_message(
        session_id: str,
        data: MessageInput
):
    agent = setup_agent(session_id)
    agent.invoke({"input": data.message})
    return {"status": "ok"}


@router.get("/conversation/")
def conversation_list():
    message_history_service = MessageHistoryService()
    conversations = message_history_service.get_unique_session_ids()
    return JSONResponse(
        content={"session_id": conversations}
    )


@router.get("/conversation/{session_id}")
def conversation_details(session_id: str):
    message_history_service = MessageHistoryService(session_id)
    return message_history_service.get_messages_by_session_id()
