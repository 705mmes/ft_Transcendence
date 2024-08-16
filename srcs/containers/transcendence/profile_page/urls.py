from django.urls import path

from . import views


urlpatterns = [
    path('', views.history),
    path('modify/', views.profile_update),
    path('deconnexion/', views.deconnexion),
]