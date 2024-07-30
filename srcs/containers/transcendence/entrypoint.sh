#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#empty db
python manage.py makemigrations
python manage.py migrate
python manage.py flush --no-input


# Create superuser if it doesn't exist
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD'),
if not User.objects.filter(username='ludo').exists():
    User.objects.create_user(username='ludo', email='ludo@maildeludo.com', password='fefe')
if not User.objects.filter(username='leon').exists():
    User.objects.create_user(username='leon', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='abel').exists():
    User.objects.create_user(username='abel', email='abel@maildeludo.com', password='caca')
if not User.objects.filter(username='dcandan').exists():
    User.objects.create_user(username='dcandan', email='dcandan@maildeludo.com', password='caca')
"
fi

exec "$@"