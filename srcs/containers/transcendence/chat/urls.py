from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    # path('chat/social/', views.social);
    # path('chat/profile/', views.profile),
    # path('chat/game/script/', views.script),
]