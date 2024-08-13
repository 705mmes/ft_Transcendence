from django.contrib import admin
from django.urls import path, include, re_path
from authentication import views
from authentication.views import register, fetch_user_data, exchange_token, StartOAuthView
from django.urls import path
urlpatterns = [
    path('', views.authentication),
    path('login_session/', views.login_session),
    path('register_session/', views.register),
    path('start-oauth/', StartOAuthView.as_view(), name='start_oauth'),
    path('exchange-token/', exchange_token, name='exchange_token'),
    path('fetch-user-data/', fetch_user_data, name='fetch_user_data'),
    path('logout_btn/', views.logout_btn),
    path('social/', views.social),
    path('api_register/', views.api_register)
]
