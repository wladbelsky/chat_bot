FROM python:3.12-slim

LABEL authors="wladbelsky"

MAINTAINER wladbelsky

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]