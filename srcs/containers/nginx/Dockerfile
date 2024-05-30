FROM debian:latest

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y nginx && apt-get install vim -y
#apt-get install openssl -y
COPY ./containers/nginx/conf/nginx.conf /etc/nginx/nginx.conf
COPY ./containers/nginx/pong/html/index.html /var/www/html/index.html
EXPOSE 8081

CMD ["nginx", "-g", "daemon off;"]