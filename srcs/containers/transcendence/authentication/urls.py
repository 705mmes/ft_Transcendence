from django.contrib import admin
from django.urls import path, include, re_path
from authentication import views

urlpatterns = [
    path('', views.authentication),
    path('login_session/', views.login_session),
    path('register_session/', views.register),
    path('api_connection/', views.api_connection),
    path('logout_btn/', views.logout_btn),
    path('social/', views.social),
]
