from django.urls import path
from . import views
    
urlpatterns = [
    path('challenge/', views.challenge_user),
    path('challenges/', views.get_user_challenges),
    path('challenge/accept/', views.accept_challenge),
    path('challenge/decline/', views.decline_challenge),
    path('', views.get_user_games),
]
