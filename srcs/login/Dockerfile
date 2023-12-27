# syntax=docker/dockerfile:1.4

FROM python:3.9.18-bookworm

EXPOSE 80

WORKDIR /app 

COPY requirements.txt /app

#COPY ./tcommons-1.0.0-py3-none-any.whl /app

RUN apt-get update

RUN apt-get install -y git postgresql-client

RUN pip3 install -r requirements.txt --no-cache-dir

ENV PYTHONUNBUFFERED=1

#RUN pip3 install tcommons-1.0.0-py3-none-any.whl

COPY . /app

CMD ["sh", "start.sh"]