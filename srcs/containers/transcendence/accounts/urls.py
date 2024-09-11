from django.urls import path
from . import views

urlpatterns = [
    path('redirect/setup/', views.redirect_to_2fa_setup, name='redirect_to_2fa_setup'),
    path('redirect/login/', views.redirect_to_login),
	path('redirect/checker/', views.redirect_to_checker),
]
