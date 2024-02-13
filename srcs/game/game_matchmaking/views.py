from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view

from .notifications.send_notification import send_friend_request_notification
from .notifications.constants import NotificationType

from django.db.models import Q
from .models import Game, GameInvite
from django.contrib.auth.models import User

# Create your views here.

@never_cache
@api_view(['POST'])
def challenge_user(request):
    opponent = request.data.get('opponent')

    if opponent is None or opponent == '':
        print('opponent is required')
        return JsonResponse({'error': 'opponent is required'}, status=400)

    try:
        opponentObj = User.objects.get(username=opponent)
    except User.DoesNotExist:
        return JsonResponse({'error': 'opponent does not exist'}, status=404)
    except:
        return JsonResponse({'error': 'error while querying the database'}, status=500)

    #Check if the user has any gamees in progress or waiting
    # game = Game.objects.filter(Q(playerLeft=request.user) | Q(playerRight=request.user)).filter(Q(status=Game.GameStatus.WAITING) | Q(status=Game.GameStatus.IN_PROGRESS))

    # game = Game.objects.create(playerLeft=request.user, playerRight=opponentObj)
    # game.save()
    invite = GameInvite.objects.create(game=None, sender=request.user, receiver=opponentObj)

    try:
        send_friend_request_notification(request.user, opponentObj, NotificationType.CHALLENGE)
    except Exception as e:
        print(e)
        print('Error while sending notification')

    return JsonResponse({'invite_id': invite.id}, status=201)

@never_cache
@api_view(['GET'])
def get_user_challenges(request):
    user = request.user

    if not user or user is None:
        return JsonResponse({'error': 'user is required'}, status=400)

    inviteStatus = request.query_params.get('status')

    try:
        invites = GameInvite.objects.filter(receiver=user)
        if inviteStatus:
            invites = invites.filter(status=inviteStatus)
    except GameInvite.DoesNotExist:
        return JsonResponse({'error': 'no invites found'}, status=404)
    except:
        return JsonResponse({'error': 'error while querying the database'}, status=500)

    invitesList = []
    for invite in invites:
        invitesList.append({
            'id': invite.id,
            'sender': invite.sender.username,
            'receiver': invite.receiver.username,
            'status': invite.status
        })
    return JsonResponse({'detail': invitesList}, status=200)

@never_cache
@api_view(['POST'])
def accept_challenge(request):
    invite_id = request.data.get('invite_id')

    if invite_id is None or invite_id == '':
        return JsonResponse({'error': 'invite_id is required'}, status=400)

    try:
        invite = GameInvite.objects.get(id=invite_id)
    except GameInvite.DoesNotExist:
        return JsonResponse({'error': 'invite does not exist'}, status=404)
    except:
        return JsonResponse({'error': 'error while querying the database'}, status=500)

    if invite.status != GameInvite.InviteStatus.PENDING:
        return JsonResponse({'error': 'invite is not pending'}, status=400)

    invite.status = GameInvite.InviteStatus.ACCEPTED
    invite.save()

    game = Game.objects.create(playerLeft=invite.sender, playerRight=invite.receiver)
    game.save()

    return JsonResponse({'game_id': game.id}, status=201)

@never_cache
@api_view(['POST'])
def decline_challenge(request):
    invite_id = request.data.get('invite_id')

    if invite_id is None or invite_id == '':
        return JsonResponse({'error': 'invite_id is required'}, status=400)

    try:
        invite = GameInvite.objects.get(id=invite_id)
    except GameInvite.DoesNotExist:
        return JsonResponse({'error': 'invite does not exist'}, status=404)
    except:
        return JsonResponse({'error': 'error while querying the database'}, status=500)

    if invite.status != GameInvite.InviteStatus.PENDING:
        return JsonResponse({'error': 'invite is not pending'}, status=400)

    invite.status = GameInvite.InviteStatus.DECLINED
    invite.save()

    return JsonResponse({'detail': 'invite declined'}, status=200)


@never_cache
@api_view(['GET'])
def get_user_games(request):
    user = request.user

    if not user or user is None:
        return JsonResponse({'error': 'user is required'}, status=400)

    #Check if the url has a query parameter for the status of the game
    gameStatus = request.query_params.get('status')
    # Check if the url has a query parameter for the opponent's username
    opponent = request.query_params.get('opponent')

    opponentObj = None

    # Get the opponent's object
    if opponent:
        try:
            opponentObj = User.objects.get(username=opponent)
        except User.DoesNotExist:
            return JsonResponse({'error': 'opponent does not exist'}, status=404)
        except:
            return JsonResponse({'error': 'error while querying the database'}, status=500)

    print('opponentObj', opponentObj)
    print('gameStatus', gameStatus)

    try:
        games = Game.objects.filter(Q(playerLeft=user) | Q(playerRight=user))
        if gameStatus:
            games = games.filter(status=gameStatus)
        if opponent and opponentObj is not None:
            games = games.filter(Q(playerLeft=opponentObj) | Q(playerRight=opponentObj))
    except Game.DoesNotExist:
        return JsonResponse({'error': 'no games found'}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'error while querying the database'}, status=500)

    print('games', games)

    gamesList = []
    for game in games:
        gamesList.append({
            'id': game.id,
            'playerLeft': game.playerLeft.username,
            'playerRight': game.playerRight.username,
            'playerLeftScore': game.playerLeftScore,
            'playerRightScore': game.playerRightScore,
            'status': game.status
        })
    return JsonResponse({'detail': gamesList}, status=200)

