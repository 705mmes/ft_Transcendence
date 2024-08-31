from django.urls import path
from . import views
from .api_views import LoginAPIView, TwoFactorSetupAPIView

urlpatterns = [
    path('two_factor/setup/start/', views.redirect_to_2fa_setup, name='get_2fa_setup_url'),
]
