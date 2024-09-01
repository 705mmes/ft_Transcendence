from django.urls import path
from . import views
from .api_views import LoginAPIView, TwoFactorSetupAPIView

urlpatterns = [
    path('two_factor/setup/start/', views.redirect_to_2fa_setup, name='get_2fa_setup'),
    path('two_factor/login/start/', views.redirect_to_2fa_login, name='get_2fa_login'),
    path('accounts/login/', views.login_view, name='login_view'),
]
