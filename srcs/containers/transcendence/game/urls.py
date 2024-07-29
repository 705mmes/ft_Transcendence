from django.urls import path

from . import views


urlpatterns = [
    path('', views.game),
    path('scripts/', views.scripts),
    path('game/scripts/', views.scripts),
]