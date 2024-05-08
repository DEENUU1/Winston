from config.settings import settings
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="",
    tags=["Chat"],
)


@router.get("/", response_class=HTMLResponse)
def input_details(request: Request):
    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name="home.html",
        # context={
        #     "details": details,
        # }
    )
