from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.conf import settings

from rest_framework.decorators import api_view

import requests

context = {
    'LOGIN_SERVICE_HOST': settings.LOGIN_SERVICE_HOST,
    'USERS_SERVICE_HOST': settings.USERS_SERVICE_HOST,
    'NOTIFICATIONS_SERVICE_HOST': settings.NOTIFICATIONS_SERVICE_HOST,
    'NOTIFICATIONS_SOCKETS_HOST': settings.NOTIFICATIONS_SOCKETS_HOST,
    'GAME_SERVICE_HOST': settings.GAME_SERVICE_HOST,
    'GAME_SOCKETS_HOST': settings.GAME_SOCKETS_HOST,
    'MATCHMAKING_SERVICE_HOST': settings.MATCHMAKING_SERVICE_HOST,
    'BASE_URL': settings.BASE_URL,
}

@never_cache
@api_view(['GET'])
def start(request):
    # Get game info from database
    auth = request.headers.get('Authorization')
    url = f'{settings.GAME_SERVICE_HOST}/'
    game_response = requests.get(url, headers={'Authorization': auth}, verify=False).json()['detail']
    context['game_info'] = {
        "player_1": game_response.playerLeft,
        "player_2": game_response.playerRight,
        "score_1": game_response.playerLeftScore,
        "score_2": game_response.playerRightScore
    }

    if request.query_params.get('opponent'):
        context['PATH'] = 'pong/?opponent=' + request.query_params.get('opponent')
    else:
        context['PATH'] = 'pong'
    
    # TO DO: request game info from database

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if auth is None and not request.user.is_authenticated:
            return redirect('/login/')
        return render(request, 'start.html', context)
    else:
        return render(request, '../templates/base.html', context)

@never_cache
@api_view(['GET'])
def lobby(request):
    if request.query_params.get('tournament_id'):
        context['PATH'] = 'lobby/?tournament_id=' + request.query_params.get('tournament_id')
    else:
        context['PATH'] = 'lobby'
    # TO DO: request game info from database
    context['waitlist'] = [
        "Player 3",
        "Player 4",
        "Player 5"
    ]
    context['game_ongoing'] = True
    context['player_1'] = "Bob"
    context['player_2'] = "Ross"
    auth = request.headers.get('Authorization')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if auth is None and not request.user.is_authenticated:
            return redirect('/login/')
        return render(request, 'lobby.html', context)
    else:
        return render(request, '../templates/base.html', context)

# class LobbyView(TemplateView):
#     template_name = 'lobby.html'
 
#     def get_context_data(self, **kwargs):
#         context = super(LobbyView, self).get_context_data(**kwargs)
#         # get current open games to prepopulate the list
 
#         return context
