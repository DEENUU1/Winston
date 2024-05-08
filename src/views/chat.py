from config.settings import settings
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from services.message_history_service import MessageHistoryService


router = APIRouter(
    prefix="",
    tags=["Chat"],
)

@router.get("/conversation/{session_id}")
def get_conversation(session_id: str):
    message_history_service = MessageHistoryService(session_id)
    conversation = message_history_service.get_messages_by_session_id()
    return [{"content": message.content, "type": message.type} for message in conversation]

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
