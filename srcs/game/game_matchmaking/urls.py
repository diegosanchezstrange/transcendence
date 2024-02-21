from django.urls import path
from . import views
    
urlpatterns = [
    path('challenge/', views.GameChallengeView.as_view()),
    # path('challenges/', views.get_user_challenges),
    path('challenge/accept/', views.accept_challenge),
    path('challenge/reject/', views.decline_challenge),
    path('', views.GameView.as_view()),
]
