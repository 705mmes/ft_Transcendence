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
from authentication.models import FriendList
from authentication.models import FriendRequest
from game.models import GameHistory
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    neo = User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD'),
if not User.objects.filter(username='ludo').exists():
    ludo = User.objects.create_user(username='ludo', email='ludo@maildeludo.com', password='fefe')
if not User.objects.filter(username='leon').exists():
    leon = User.objects.create_user(username='leon', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='abel').exists():
    abel = User.objects.create_user(username='abel', email='abel@maildeludo.com', password='caca')
if not User.objects.filter(username='dcandan').exists():
    dcandan = User.objects.create_user(username='dcandan', email='dcandan@maildeludo.com', password='caca')
if not FriendRequest.objects.filter(requester=leon, recipient=ludo):
    FriendRequest.objects.create(requester=leon, recipient=ludo)
if not FriendRequest.objects.filter(requester=leon, recipient=dcandan):
    FriendRequest.objects.create(requester=leon, recipient=dcandan)
#if not FriendList.objects.filter(user1=leon, user2=ludo).exists():
#    FriendList.objects.create(user1=leon, user2=ludo)
if not FriendList.objects.filter(user1=leon, user2=abel).exists():
    FriendList.objects.create(user1=leon, user2=abel)
if not FriendList.objects.filter(user1=ludo, user2=dcandan).exists():
    FriendList.objects.create(user1=ludo, user2=dcandan)
if not FriendRequest.objects.filter(requester=leon, recipient=ludo):
    FriendRequest.objects.create(requester=leon, recipient=ludo)
GameHistory.objects.create(History1=leon, History2=ludo, Score1=3, Score2=0)
GameHistory.objects.create(History1=dcandan, History2=leon, Score1=0, Score2=3)
GameHistory.objects.create(History1=dcandan, History2=ludo, Score1=3, Score2=2)
GameHistory.objects.create(History1=leon, History2=dcandan, Score1=1, Score2=2)
GameHistory.objects.create(History1=leon, History2=dcandan, Score1=30, Score2=1)
GameHistory.objects.create(History1=leon, History2=dcandan, Score1=30, Score2=1)
GameHistory.objects.create(History1=leon, History2=dcandan, Score1=30, Score2=4)
GameHistory.objects.create(History1=leon, History2=dcandan, Score1=30, Score2=5)
GameHistory.objects.create(History1=leon, History2=dcandan, Score1=30, Score2=6)
GameHistory.objects.create(History1=leon, History2=dcandan, Score1=30, Score2=7)
"
fi

exec "$@"