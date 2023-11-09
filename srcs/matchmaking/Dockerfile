# syntax=docker/dockerfile:1.4

FROM python AS builder

EXPOSE 8083

WORKDIR /app 

COPY requirements.txt /app

RUN apt-get update

RUN apt-get install git

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app 

ENTRYPOINT ["python3"] 

CMD ["manage.py", "runserver", "0.0.0.0:8080"]
