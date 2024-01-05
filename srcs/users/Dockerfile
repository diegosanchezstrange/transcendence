# syntax=docker/dockerfile:1.4

FROM python:3.9-alpine

EXPOSE 80

WORKDIR /app 

COPY requirements.txt /app

RUN apk update

RUN apk add git postgresql-client

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["sh", "start.sh"]
