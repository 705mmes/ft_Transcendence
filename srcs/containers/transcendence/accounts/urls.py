from django.urls import path
from . import views

urlpatterns = [
    path('two_factor/setup/start/', views.redirect_to_2fa_setup),
    path('redirect/login/', views.redirect_to_login),
	path('redirect/checker/', views.redirect_to_checker),
    path('login/', views.two_factor_login),
]
