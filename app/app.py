from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import FileResponse
from ml.model import load_model
import pandas as pd
from fastapi import Body
from io import StringIO, BytesIO
import os
from fastapi.responses import StreamingResponse
import io

model = None
app = FastAPI()

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


@app.post("/upload",response_class=StreamingResponse)
async def upload_file(file: UploadFile = File(...)):
    contents = file.file.read() # Read the contents of the uploaded file
    data = BytesIO(contents) # Store the contents in a BytesIO object
    #df = pd.read_csv(data,sep=',') # Convert BytesIO object to Pandas DataFrame
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

