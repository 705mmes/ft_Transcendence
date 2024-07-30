from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path('social/', views.social, name="social"),
    path('profile/', views.profile, name="profile"),
    path('game/', views.game, name="game"),
]