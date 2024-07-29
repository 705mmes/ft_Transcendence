from django.urls import path

from . import views


urlpatterns = [
    path('', views.game),
    path('game/', views.game),
    path('game_reload', views.game_reload),
    path('scripts/', views.scripts),
]