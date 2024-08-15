from django.contrib import admin
from django.urls import path, include, re_path
from authentication import views
from authentication.views import register, start_oauth2_flow, oauth_callback, register_api
from django.urls import path
urlpatterns = [
    path('', views.authentication),
    path('login_session/', views.login_session),
    path('register_session/', views.register),
    path('oauth/start/', views.start_oauth2_flow, name='start_oauth2_flow'),
    path('oauth/callback/', views.oauth_callback, name='oauth_callback'),
    path('register_api/', views.register_api, name='register_api'),
    path('logout_btn/', views.logout_btn),
    path('social/', views.social),
]
