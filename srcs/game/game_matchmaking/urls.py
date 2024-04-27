from django.urls import path
from . import views
    
urlpatterns = [
    path('challenge/', views.GameChallengeView.as_view()),
    # path('challenges/', views.get_user_challenges),
    path('challenge/accept/', views.accept_challenge),
    path('challenge/reject/', views.decline_challenge),
    path('game/<int:id>/', views.get_user_games),
    path('game/', views.create_game),
    path('tournament/', views.GameTournamentView.as_view()),
    path('tournament/player/status/', views.user_tournament_status),
    path('tournament/players/', views.get_top_players),
    path('tournament/<int:id>/matches/', views.get_tournament_matches),
    path('tournament/nextgame/', views.next_tournament_game),
]
