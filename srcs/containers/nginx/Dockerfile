FROM debian:latest

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y nginx vim openssl
RUN mkdir -p /etc/nginx/ssl

# Generate SSL certificates
RUN openssl req -x509 -nodes \
    -keyout /etc/nginx/ssl/transcendence.key \
    -out /etc/nginx/ssl/transcendence.crt \
    -subj "/C=FR/ST=IDF/L=Paris/O=42/OU=42/CN=smunio.42.fr"

EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]