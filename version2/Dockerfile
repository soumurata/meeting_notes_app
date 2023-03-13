FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get -y install ffmpeg

COPY . .

CMD streamlit run app.py