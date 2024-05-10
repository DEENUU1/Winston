from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.settings import settings
from routers.router import router
from tasks import create_providers, create_llms, create_tools, create_agents, create_settings
from utils.init_db import create_tables

app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
)

app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initializes the database tables when the application starts up.
    """
    create_tables()
    create_providers.create_providers()
    create_llms.create_llms()
    create_tools.create_tools()
    create_agents.create_agents()
    create_settings.create_settings()


app.include_router(router)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
