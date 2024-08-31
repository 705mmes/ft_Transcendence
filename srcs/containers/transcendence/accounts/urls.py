from django.urls import path
from .api_views import LoginAPIView, TwoFactorSetupAPIView

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/setup-2fa/', TwoFactorSetupAPIView.as_view(), name='api-setup-2fa'),
]
