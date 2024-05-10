from fastapi import APIRouter
from . import conversation, provider, llm, tool, settings


router = APIRouter(
    prefix=""
)

router.include_router(conversation.router)
router.include_router(provider.router)
router.include_router(llm.router)
router.include_router(tool.router)
router.include_router(settings.router)
