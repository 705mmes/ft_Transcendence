FROM debian:latest

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y nginx vim openssl
RUN mkdir -p /etc/nginx/ssl

# Generate SSL certificates
RUN openssl req -x509 -nodes -out /etc/nginx/ssl/transcendence.crt -keyout /etc/nginx/ssl/transcendence.key -subj "/C=FR/ST=IDF/L=Paris/O=42/OU=42/CN=smunio.42.fr/UID=smunio"
RUN chmod 755 -R /var/www
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]