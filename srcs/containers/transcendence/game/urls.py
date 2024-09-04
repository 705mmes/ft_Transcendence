from django.urls import path

from . import views


urlpatterns = [
    path('', views.game, name='game'),
    path('canvas/', views.canvas),
    path('scripts/', views.scripts),
   # path('social/', views.social, name='social'),
   # path('chat/', views.chat, name='chat'),
]