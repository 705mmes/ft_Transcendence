#!/bin/sh

# Remplacer les placeholders par les variables d'environnement
envsubst < /pgadmin_setup/servers.json.template > /var/lib/pgadmin/pgadmin4/servers.json

# Démarrer PgAdmin
/entrypoint.sh