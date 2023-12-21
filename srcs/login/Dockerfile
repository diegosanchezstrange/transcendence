# syntax=docker/dockerfile:1.4

FROM python AS builder

EXPOSE 8080

WORKDIR /app 

COPY requirements.txt /app

#COPY ./tcommons-1.0.0-py3-none-any.whl /app

RUN apt-get update

RUN apt-get install git

RUN pip3 install -r requirements.txt --no-cache-dir

ENV PYTHONUNBUFFERED=1

#RUN pip3 install tcommons-1.0.0-py3-none-any.whl

COPY . /app

CMD ["sh", "start.sh"]
