# myapp/urls.py
from django.urls import path
from .views import register_player, update_score

urlpatterns = [
    path('register/', register_player, name='register_player'),
    path('update_score/', update_score, name='update_score'),
]