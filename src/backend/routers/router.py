from fastapi import APIRouter
from . import conversation

router = APIRouter(
    prefix=""
)

router.include_router(conversation.router)
