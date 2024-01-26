FROM nginx:1.24.0-alpine

EXPOSE 443 

RUN apk update && apk add openssl
RUN openssl req -x509 -nodes -days 365 -subj "/ST=Spain/L=Madrid/OU=42Madrid/CN=manmarti" -newkey rsa:2048 -out /etc/ssl/ssl.crt -keyout /etc/ssl/ssl.key

COPY ./default.conf /etc/nginx/conf.d/default.conf
