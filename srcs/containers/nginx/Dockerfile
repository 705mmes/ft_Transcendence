FROM debian:latest

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y nginx && apt-get install vim -y && apt-get install openssl -y
RUN mkdir -p /etc/nginx/ssl
RUN openssl req -x509 -nodes -out /etc/nginx/ssl/transcendence.crt -keyout /etc/nginx/ssl/transcendence.key -subj "/C=FR/ST=IDF/L=Paris/O=42/OU=42/CN=login.42.fr/UID=smunio"
COPY ./containers/nginx/conf/nginx.conf /etc/nginx/nginx.conf
COPY ./containers/nginx/pong/html/index.html /var/www/html/index.html
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]