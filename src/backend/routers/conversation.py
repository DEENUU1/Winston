from fastapi import APIRouter, Form, Response
from fastapi.responses import HTMLResponse

from ai.main import setup_agent
from services.message_history_service import MessageHistoryService

router = APIRouter(
    prefix="",
    tags=["Conversation"],
)


@router.post("/conversation/search/")
def search_conversations(
        query: str = Form(...)
):
    message_history_service = MessageHistoryService()
    conversations = message_history_service.search_conversations_by_content(query)
    return conversations


@router.post("/conversation/{session_id}")
def send_message(
        response: Response,
        session_id: str,
        user_input: str = Form(...),
):
    response.headers["HX-Refresh"] = "true"
    agent = setup_agent(session_id)
    agent.invoke({"input": user_input})
    return {"status": "ok"}


@router.get("/conversation/", response_class=HTMLResponse)
def conversation_list():
    message_history_service = MessageHistoryService()
    conversations = message_history_service.get_unique_session_ids()
    return conversations


@router.get("/conversation/{session_id}")
def conversation_details(session_id: str):
    message_history_service = MessageHistoryService(session_id)
    return message_history_service.get_messages_by_session_id()
