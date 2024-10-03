import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendence.settings')

# Initialize Django ASGI application
application = get_asgi_application()

# Now that Django is initialized, import routing and consumers
from authentication.routing import websocket_urlpatterns as authentication_websocket_urlpatterns
from game.routing import websocket_urlpatterns as game_websocket_urlpatterns

# Combine all routing into a single application
application = ProtocolTypeRouter({
    "http": application,  # Already initialized application
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                authentication_websocket_urlpatterns + game_websocket_urlpatterns
            )
        )
    )
})
