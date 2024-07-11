from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.authentication, name='authentication'),
    path('login_session/', views.login_session, name='login_session'),
    path('logout_btn/', views.logout_btn, name='logout_btn'),
    path('select_game/', views.select_game, name='select_game'),
    path('game/<str:room_name>/', views.game, name='game'),
]



# from django.contrib import admin
# from django.urls import path, include
# from authentication import views
#
# urlpatterns = [
#     path('', views.authentication),
#     path('login_session/', views.login_session),
#     path('logout_btn/', views.logout_btn),
#     path('game/', views.game),
# ]
