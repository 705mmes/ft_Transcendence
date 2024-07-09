from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('', views.authentication),
    path('login_session/', views.login_session),
    path('logout_btn/', views.logout_btn),
    path('game/', views.game),
]
