from django.urls import re_path
from authentication.consumers import ActiveConsumer

websocket_urlpatterns = [
    re_path(r"ws/authentication/social/$", ActiveConsumer.as_asgi()),
]