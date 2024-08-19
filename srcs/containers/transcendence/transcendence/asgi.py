"""
ASGI config for transcendence project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.urls import path
from authentication.consumers import ActiveConsumer
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from authentication.routing import websocket_urlpatterns as authentication_websocket_urlpatterns
from game.routing import websocket_urlpatterns as game_websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendence.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                authentication_websocket_urlpatterns + game_websocket_urlpatterns
            )
        )
    )
})
