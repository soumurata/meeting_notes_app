FROM python:3

COPY requirements.txt .

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install notebook

RUN apt-get update && \
    apt-get -y install ffmpeg


WORKDIR /app

COPY . .

EXPOSE 8501

CMD streamlit run app.py