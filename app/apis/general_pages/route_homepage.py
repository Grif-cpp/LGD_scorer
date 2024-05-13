from fastapi import Request,APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pathlib
from fastapi.responses import StreamingResponse

BASE_DIR = pathlib.Path(__file__).parent.parent.parent

templates = Jinja2Templates(directory= BASE_DIR / "templates")
general_pages_router = APIRouter()


@general_pages_router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("general_pages/homepage.html",{"request":request})
    #return templates.TemplateResponse("shared/base.html",{"request":request})