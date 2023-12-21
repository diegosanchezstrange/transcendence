# syntax=docker/dockerfile:1.4

FROM python:3.13-rc-bookworm

EXPOSE 8082

WORKDIR /app 

COPY requirements.txt /app

RUN apt-get update

RUN apt-get install git

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["sh", "start.sh"]