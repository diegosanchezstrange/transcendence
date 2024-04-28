from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.conf import settings

from rest_framework.decorators import api_view
from django.http import JsonResponse

import requests

context = {
    'LOGIN_SERVICE_HOST': settings.LOGIN_SERVICE_HOST,
    'USERS_SERVICE_HOST': settings.USERS_SERVICE_HOST,
    'NOTIFICATIONS_SERVICE_HOST': settings.NOTIFICATIONS_SERVICE_HOST,
    'NOTIFICATIONS_SOCKETS_HOST': settings.NOTIFICATIONS_SOCKETS_HOST,
    'GAME_SERVICE_HOST': settings.GAME_SERVICE_HOST,
    'GAME_SERVICE_HOST_INTERNAL': settings.GAME_SERVICE_HOST_INTERNAL,
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
    id = request.user.id
    print(id)
    user_matches = requests.get(
        f'{settings.GAME_SERVICE_HOST_INTERNAL}/game/{id}/',
        headers={'Authorization': auth},
        verify=False)

    if user_matches.status_code != 200:
        context['PATH'] = 'home'
        return render(request, '../templates/base.html', context)
    user_matches = user_matches.json()['detail']

    current_game = None
    for match in user_matches:
        if match['status'] != 'FINISHED':
            current_game = match
    if current_game == None:
        return redirect('/home/')

    context['game_info'] = {
        "player_1": current_game['playerLeft'],
        "player_2": current_game['playerRight']
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

    auth = request.headers.get('Authorization')
    tournament_id = request.query_params.get('tournament')
    try:
        players = requests.get(
            f'{settings.GAME_SERVICE_HOST_INTERNAL}/tournament/players/?tournament_id={tournament_id}',
            headers={'Authorization': auth},
            verify=False)
        players = players.json()["players"]
        current_game = requests.get(
            f'{settings.GAME_SERVICE_HOST_INTERNAL}/tournament/nextgame/',
            headers={'Authorization': auth},
            verify=False)
        current_game = current_game.json()['game']
        context['player3'] = None
        for player in players:
            if player['username'] == current_game['playerLeft']:
                context['playerLeft'] = players['username']
            elif player['username'] == current_game['playerRight']:
                context['playerRight'] = players['username']
            elif context['player3'] == None:
                context['player3'] = players['username']
            else:
                context['player4'] = players['username']
    except Exception as e:
        print(e)
        print(e.message)
        return JsonResponse({
            "message": "Players not found."
            }, status=404)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if auth is None and not request.user.is_authenticated:
            return redirect('/login/')
        return render(request, 'lobby.html', context)
    else:
        return render(request, '../templates/base.html', context)

