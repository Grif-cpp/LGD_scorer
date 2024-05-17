from fastapi import FastAPI, UploadFile, File, APIRouter
from pydantic import BaseModel
from io import StringIO, BytesIO
from fastapi.responses import StreamingResponse
import io

import pathlib
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ml.model import *

from app.core.config import *
from app.apis.general_pages.route_homepage import general_pages_router

BASE_DIR = pathlib.Path(__file__).parent

def include_router(app):
    app.include_router(general_pages_router)


def start_application():
    app = FastAPI(title=PROJECT_NAME,version=PROJECT_VERSION)
    include_router(app)
    return app


model_connector = ModelConnector()
app = start_application()
# добавление статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/upload", response_class=StreamingResponse)
async def upload_file(file: UploadFile = File(...)):
    contents = file.file.read() # Read the contents of the uploaded file
    data = BytesIO(contents) # Store the contents in a BytesIO object
    score = model_connector.send_and_recieve_data(data).pred
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


