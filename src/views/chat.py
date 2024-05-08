from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse

from ai.main import setup_agent
from config.settings import settings
from services.message_history_service import MessageHistoryService

router = APIRouter(
    prefix="",
    tags=["Chat"],
)


@router.get("/conversation/{session_id}")
def get_conversation(session_id: str):
    message_history_service = MessageHistoryService(session_id)
    conversation = message_history_service.get_messages_by_session_id()
    return [{"content": message.content, "type": True if message.type == "human" else False} for message in
            conversation]


@router.post("/conversation/search/")
def search_conversations(
        query: str = Form(...)
):
    print(query)
    message_history_service = MessageHistoryService()
    conversations = message_history_service.search_conversations_by_content(query)
    return conversations


@router.post("/conversation/{session_id}")
def send_message(
        session_id: str,
        user_input: str = Form(...),
):
    agent = setup_agent(session_id)
    agent.invoke({"input": user_input})
    return {"status": "ok"}


@router.get("/", response_class=HTMLResponse)
def chat(request: Request):
    message_history_service = MessageHistoryService()

    conversations = message_history_service.get_unique_session_ids()

    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "conversations": conversations,
        }
    )
