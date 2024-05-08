from fastapi import APIRouter
from . import chat

router = APIRouter(
    prefix=""
)

router.include_router(chat.router)
