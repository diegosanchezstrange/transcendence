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
    if request.query_params.get('opponent'):
        context['PATH'] = 'pong/?opponent=' + request.query_params.get('opponent')
    else:
        context['PATH'] = 'pong'
    auth = request.headers.get('Authorization')
    # TO DO: request game info from database
    context['game_info'] = {
        "player_1": "Player 1",
        "player_2": "Player 2",
        "score_1": "0",
        "score_2": "0"
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if auth is None and not request.user.is_authenticated:
            return redirect('/login/')
        return render(request, 'start.html', context)
    else:
        return render(request, '../templates/base.html', context)

@never_cache
@api_view(['GET'])
def lobby(request):
    print(request.query_params)
    if request.query_params.get('tournament'):
        context['PATH'] = 'lobby/?tournament=' + request.query_params.get('tournament')
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
