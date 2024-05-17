FROM python:3.9-slim

WORKDIR .

COPY . .

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port","8082"]