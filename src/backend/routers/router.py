from fastapi import APIRouter
from . import conversation, llm, tool, settings, agent, snippet, file


router = APIRouter(
    prefix=""
)

router.include_router(conversation.router)
router.include_router(llm.router)
router.include_router(tool.router)
router.include_router(settings.router)
router.include_router(agent.router)
router.include_router(snippet.router)
router.include_router(file.router)
