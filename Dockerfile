FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port","80"]