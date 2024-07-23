FROM nginx:latest

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y nginx vim openssl
RUN rm -f /etc/nginx/conf.d/default.conf
COPY ./conf/nginx.conf /etc/nginx/conf.d