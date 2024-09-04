from django.urls import path

from . import views


urlpatterns = [
    path('', views.history),
    path('modify/', views.profile_update, name='profile_modify'),
    path('friend_profile/', views.friend_profile),
]