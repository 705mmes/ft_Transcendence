from django.urls import path

from . import views


urlpatterns = [
    path('', views.game),
    path('canvas/', views.canvas),
    path('scripts/', views.scripts),
]