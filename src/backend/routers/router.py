from fastapi import APIRouter
from . import conversation, provider


router = APIRouter(
    prefix=""
)

router.include_router(conversation.router)
router.include_router(provider.router)
