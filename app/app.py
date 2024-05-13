from fastapi import FastAPI, UploadFile, File, APIRouter
from pydantic import BaseModel
from ml.model import load_model
from io import StringIO, BytesIO
from fastapi.responses import StreamingResponse
import io

import pathlib
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.core.config import *
from app.apis.general_pages.route_homepage import general_pages_router

BASE_DIR = pathlib.Path(__file__).parent

def include_router(app):
    app.include_router(general_pages_router)


def start_application():
    app = FastAPI(title=PROJECT_NAME,version=PROJECT_VERSION)
    include_router(app)
    return app


##### HTML

model = None
app = start_application()
app.mount("/static", StaticFiles(directory= "static"), name="static")



# формат ответа от модели
class ModelResponse(BaseModel):
    LGD_predictions: str

    class Config:
        arbitrary_types_allowed = True


# запуск функции при при запуске app
@app.on_event("startup")
def startup_event():
    global model
    model = load_model()


@app.post("/upload", response_class=StreamingResponse)
async def upload_file(file: UploadFile = File(...)):
    contents = file.file.read() # Read the contents of the uploaded file
    data = BytesIO(contents) # Store the contents in a BytesIO object
    score = model(data).pred
    data.close()  # Close the BytesIO object
    file.file.close()  # Close the uploaded file

    def export_data(df):
        stream = io.StringIO()
        df.to_csv(stream, index=False,sep=';')
        response = StreamingResponse(
            iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response

    return export_data(score)

# HTML часть

'''BASE_DIR = pathlib.Path(__file__).parent

templates = Jinja2Templates(directory=[
    BASE_DIR / "templates",
])

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    posts = [
        {"id":1, "title":"fastapi.blog title 1", "body":"Learn FastAPI with the fastapi.blog team 1"},
        {"id":2, "title":"fastapi.blog title 2", "body":"Learn FastAPI with the fastapi.blog team 2"},
        {"id":3, "title":"fastapi.blog title 3", "body":"Learn FastAPI with the fastapi.blog team 3"},
    ]
    context = {
        "request": request,
        "posts": posts,
        "title": "Home Page"
    }
    response = templates.TemplateResponse("index.html", context)
    return response
'''


