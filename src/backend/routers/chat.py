from fastapi import Request, APIRouter, Form, Response
from fastapi.responses import HTMLResponse

from backend.ai.main import setup_agent
from backend.config.settings import settings
from backend.services.message_history_service import MessageHistoryService

router = APIRouter(
    prefix="",
    tags=["Chat"],
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


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    message_history_service = MessageHistoryService()

    conversations = message_history_service.get_unique_session_ids()

    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "conversations": conversations,
        }
    )


@router.get("/conversation/{session_id}")
def conversation(session_id: str):
    message_history_service = MessageHistoryService(session_id)
    return message_history_service.get_messages_by_session_id()
