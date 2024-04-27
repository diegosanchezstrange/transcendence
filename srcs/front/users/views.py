from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.conf import settings
from django.views.decorators.cache import never_cache

from rest_framework.decorators import api_view

import requests
from django.http import JsonResponse

# Create your views here.

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
def profile(request):
    user = request.user
    id = user.id
    context['PATH'] = 'profile'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            auth = request.headers.get('Authorization')
            
            

            user_info = requests.get(
                settings.USERS_SERVICE_HOST_INTERNAL + "/profile/",
                  headers={'Authorization': auth},
                    verify=False
                    ).json()['detail']

            try:
                user_matches = requests.get(
                    f'{settings.GAME_SERVICE_HOST_INTERNAL}/game/{id}/',
                     headers={'Authorization': auth},
                     verify=False
                    ).json()['detail']
                
                # Mock match
                # user_matches.append({
                # 'id': 1,
                # 'playerLeft': "bob",
                # 'playerRight': "wob",
                # 'playerLeftId': 1,
                # 'playerRightId': 2,
                # 'playerLeftScore': 5,
                # 'playerRightScore': 2,
                # 'winner': "bob",
                # 'status': 'FINISHED'
                # })

                last_matches = []
                num_matches = 5 if len(user_matches) > 5 else len(user_matches)
                for i in range(num_matches):
                    match = user_matches[i]
                    last_matches.append({
                        'Left player': match['playerLeft'],
                        'Left player score': match['playerLeftScore'],
                        'Right player': match['playerRight'],
                        'Right player score': match['playerRightScore'],
                    })

                user_info['matches'] = last_matches
                
                num_games = 0
                num_wins = 0
                num_loses = 0
                for match in user_matches:
                    num_games += 1
                    if match['winner'] == user:
                        num_wins += 1
                    else:
                        num_loses += 1
                user_info['games_played'] = num_games
                user_info['wins'] = num_wins
                user_info['loses'] = num_loses
            except Exception as e:
                print(e)
                return JsonResponse({
                    "message": "Matches not found."
                    }, status=404)

            context['user_info'] = user_info
            return render(request, 'userProfile.html', context)
        else:
            # Redirect to login page with a 302 status
            return redirect("/login/")
    else:
        return render(request, 'base.html', context)

@never_cache
@api_view(['GET'])
def user_profile(request, id):
    context['PATH'] = f'profile/{id}'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            auth = request.headers.get('Authorization')
            user_response = requests.get(settings.USERS_SERVICE_HOST_INTERNAL + f"/profile/user/{id}/", headers={'Authorization': auth}, verify=False)
            if user_response.status_code == 404:
                return render(request, 'userNotFound.html', context)
            else:
                user_info = user_response.json()['detail']
            
            try:
                user_matches = requests.get(
                    f'{settings.GAME_SERVICE_HOST_INTERNAL}/game/{id}/',
                     headers={'Authorization': auth},
                     verify=False
                    ).json()['detail']
                
                # Mock match
                # user_matches.append({
                # 'id': 1,
                # 'playerLeft': "bob",
                # 'playerRight': "wob",
                # 'playerLeftId': 1,
                # 'playerRightId': 2,
                # 'playerLeftScore': 5,
                # 'playerRightScore': 2,
                # 'winner': "bob",
                # 'status': 'FINISHED'
                # })

                last_matches = []
                num_matches = 5 if len(user_matches) > 5 else len(user_matches)
                for i in range(num_matches):
                    match = user_matches[i]
                    last_matches.append({
                        'Left player': match['playerLeft'],
                        'Left player score': match['playerLeftScore'],
                        'Right player': match['playerRight'],
                        'Right player score': match['playerRightScore'],
                    })

                user_info['matches'] = last_matches
                
                num_games = 0
                num_wins = 0
                num_loses = 0
                for match in user_matches:
                    num_games += 1
                    if match['winner'] == User.objects.get(id=id):
                        num_wins += 1
                    else:
                        num_loses += 1
                user_info['games_played'] = num_games
                user_info['wins'] = num_wins
                user_info['loses'] = num_loses
            except Exception as e:
                print(e)
                return JsonResponse({
                    "message": "Matches not found."
                    }, status=404)

            context['user_info'] = user_info

            return render(request, 'userProfileNonEditable.html', context)
        else:
            # Redirect to login page with a 302 status
            return redirect("/login/")
    else:
        return render(request, 'base.html', context)
