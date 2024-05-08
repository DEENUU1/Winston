from config.settings import settings
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from services.message_history_service import MessageHistoryService


router = APIRouter(
    prefix="",
    tags=["Chat"],
)


@router.get("/", response_class=HTMLResponse)
def chat(request: Request):
    message_history_service = MessageHistoryService()

    conversations = message_history_service.get_unique_session_ids()
    print(conversations)
    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "conversations": conversations,
        }
    )
