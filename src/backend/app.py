from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.settings import settings
from utils.init_db import create_tables
from routers.router import router

app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initializes the database tables when the application starts up.
    """
    create_tables()


app.include_router(router)
