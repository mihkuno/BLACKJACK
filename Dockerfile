FROM python:3.8.18-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

CMD uvicorn main:app --reload --port=8000 --host=0.0.0.0