from fastapi import Request,APIRouter
from fastapi.templating import Jinja2Templates
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent.parent

templates = Jinja2Templates(directory= BASE_DIR / "templates")
general_pages_router = APIRouter()

@general_pages_router.get("/")
async def home(request: Request):
    print('HOME')
    return templates.TemplateResponse("general_pages/homepage.html",{"request":request})