from django.urls import re_path
from .consumers import GameConsumer, AsyncConsumer

websocket_urlpatterns = [
    re_path(r"ws/game/game/", GameConsumer.as_asgi()),
    re_path(r"ws/game/match/", AsyncConsumer.as_asgi()),
]