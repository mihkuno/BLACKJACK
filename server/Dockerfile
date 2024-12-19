FROM python:3.12.2-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

RUN pip install -r requirements.txt

CMD gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
