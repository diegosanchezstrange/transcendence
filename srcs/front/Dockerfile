# syntax=docker/dockerfile:1.4

FROM python:3.9-alpine AS builder

EXPOSE  80

WORKDIR /app 

COPY requirements.txt /app

RUN apk update

RUN apk add git

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app 

ENTRYPOINT ["python3"] 

CMD ["manage.py", "runserver", "0.0.0.0:80"]
