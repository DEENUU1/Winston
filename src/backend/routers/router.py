from fastapi import APIRouter
from . import conversation, provider, llm, tool


router = APIRouter(
    prefix=""
)

router.include_router(conversation.router)
router.include_router(provider.router)
router.include_router(llm.router)
router.include_router(tool.router)
