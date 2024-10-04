# in your routing.py file
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from authentication.consumers import ActiveConsumer
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    re_path(r"ws/authentication/social/$", ActiveConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "http": get_asgi_application(),  # Ensure you have this for regular HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})