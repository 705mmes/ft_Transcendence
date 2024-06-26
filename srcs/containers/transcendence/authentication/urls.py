from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('', views.authentication),
    path('login_popup/', views.login_popup),
    path('registration_popup/', views.registration_popup),
    path('login_session/', views.login_session)
]
