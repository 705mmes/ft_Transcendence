#!/bin/sh

# Ensure the directory exists
mkdir -p /var/lib/pgadmin/pgadmin4/

# Replace placeholders with environment variables using sed
sed -e "s/\${POSTGRES_DB}/$POSTGRES_DB/" \
    -e "s/\${POSTGRES_USER}/$POSTGRES_USER/" \
    -e "s/\${POSTGRES_PASSWORD}/$POSTGRES_PASSWORD/" \
    -e "s/\${PGADMIN_DEFAULT_EMAIL}/$PGADMIN_DEFAULT_EMAIL/" \
    -e "s/\${PGADMIN_DEFAULT_PASSWORD}/$PGADMIN_DEFAULT_PASSWORD/" \
    /pgadmin_setup/servers.json.template > /var/lib/pgadmin/pgadmin4/servers.json

# Start PgAdmin
/entrypoint.sh
