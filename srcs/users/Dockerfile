# syntax=docker/dockerfile:1.4

FROM python:3.9.18-bookworm

EXPOSE 8082

WORKDIR /app 

COPY requirements.txt /app

RUN apt-get update

RUN apt-get -y install git postgresql-client

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["sh", "start.sh"]