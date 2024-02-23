from django.urls import path
from . import views
    
urlpatterns = [
    path('challenge/', views.GameChallengeView.as_view()),
    # path('challenges/', views.get_user_challenges),
    path('challenge/accept/', views.accept_challenge),
    path('challenge/reject/', views.decline_challenge),
    path('', views.GameView.as_view()),
    path('tournament/', views.GameTournamentView.as_view()),
    path('tournament/players/', views.get_tournament_players),
    path('tournament/<int:id>/matches/', views.get_tournament_matches),
    path('tournament/nextgame/', views.next_tournament_game),
]
