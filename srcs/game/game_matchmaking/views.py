from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view
from functools import wraps
from django.utils.decorators import method_decorator

from .notifications.send_notification import send_friend_request_notification
from .notifications.constants import NotificationType

from rest_framework.views import APIView

from django.db.models import Q
from .models import Game, GameInvite
from django.contrib.auth.models import User

from django.conf import settings

def private_microservice_endpoint(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        api_token = request.headers.get('Authorization')
        print('api_token')
        print(api_token)
        if not api_token or api_token != settings.MICROSERVICE_API_TOKEN:
            return JsonResponse({'detail': 'Invalid API token.'}, status=401)
        return f(request, *args, **kwargs)
    return decorated_function

# Create your views here.


@method_decorator(never_cache, name='dispatch')
class GameView(APIView):

    @method_decorator(private_microservice_endpoint)
    def post(self, request):
        print('create_game')
        playerLeft = request.data.get('playerLeft')
        playerRight = request.data.get('playerRight')

        print(playerLeft)
        print(playerRight)

        if playerLeft is None or playerLeft == '' or playerRight is None or playerRight == '':
            return JsonResponse({'error': 'playerLeft and playerRight are required'}, status=400)

        try:
            playerLeftObj = User.objects.get(id=playerLeft)
            playerRightObj = User.objects.get(id=playerRight)

            # Check if a Game already exists for the user and are waiting, IN_PROGRESS or PAUSED
            game = Game.objects.filter(Q(playerLeft=playerLeftObj) | Q(playerRight=playerLeftObj)).filter(Q(status=Game.GameStatus.WAITING) | Q(status=Game.GameStatus.IN_PROGRESS) | Q(status=Game.GameStatus.PAUSED))
            if game.exists():
                return JsonResponse({'error': 'game already exists'}, status=409)
            game = Game.objects.filter(Q(playerLeft=playerRightObj) | Q(playerRight=playerRightObj)).filter(Q(status=Game.GameStatus.WAITING) | Q(status=Game.GameStatus.IN_PROGRESS) | Q(status=Game.GameStatus.PAUSED))
            if game.exists():
                return JsonResponse({'error': 'game already exists'}, status=409)
        except User.DoesNotExist:
            return JsonResponse({'error': 'player does not exist'}, status=404)
        except:
            return JsonResponse({'error': 'error while querying the database'}, status=500)

        game = Game.objects.create(playerLeft=playerLeftObj, playerRight=playerRightObj)
        game.save()

        return JsonResponse({'game_id': game.id}, status=201)

    def get(self, request):
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

        gamesList = []
        for game in games:
            gamesList.append({
                'id': game.id,
                'playerLeft': game.playerLeft.username,
                'playerRight': game.playerRight.username,
                'playerLeftId': game.playerLeft.id,
                'playerRightId': game.playerRight.id,
                'playerLeftScore': game.playerLeftScore,
                'playerRightScore': game.playerRightScore,
                'status': game.status
            })
        return JsonResponse({'detail': gamesList}, status=200)


@method_decorator(never_cache, name='dispatch')
class GameChallengeView(APIView):

    def post(self,request):
        opponent = request.data.get('opponent')

        if opponent is None or opponent == '':
            return JsonResponse({'error': 'opponent is required'}, status=400)

        # Check if a Game already exists for the user and are waiting, IN_PROGRESS or PAUSED
        try:
            game = Game.objects.filter(Q(playerLeft=request.user) | Q(playerRight=request.user)).filter(Q(status=Game.GameStatus.WAITING) | Q(status=Game.GameStatus.IN_PROGRESS) | Q(status=Game.GameStatus.PAUSED))
            if game.exists():
                return JsonResponse({'error': 'game already exists'}, status=409)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'error while querying the database'}, status=500)

        try:
            opponentObj = User.objects.get(id=opponent)
        except User.DoesNotExist:
            print('opponent does not exist')
            return JsonResponse({'error': 'opponent does not exist'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'error while querying the database'}, status=500)

        try:
            oldInvite = GameInvite.objects.filter(sender=request.user, receiver=opponentObj).filter(status=GameInvite.InviteStatus.PENDING)
            if oldInvite.exists():
                return JsonResponse({'error': 'invite already sent'}, status=409)
            invite = GameInvite.objects.create(game=None, sender=request.user, receiver=opponentObj)
            invite.save()
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'error while creating the invite'}, status=500)

        try:
            send_friend_request_notification(request.user, opponentObj, NotificationType.CHALLENGE)
        except Exception as e:
            print(e)
            print('Error while sending notification')

        return JsonResponse({'invite_id': invite.id}, status=201)

    def get(self, request):
        user = request.user

        if not user or user is None:
            return JsonResponse({'error': 'user is required'}, status=400)

        inviteStatus = request.query_params.get('status')
        opponent = request.query_params.get('opponent')

        try:
            invites = GameInvite.objects.filter(receiver=user)
            if opponent:
                opponentObj = User.objects.get(username=opponent)
                invites = GameInvite.objects.filter(receiver=opponentObj, sender=user)
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
        print(invitesList)
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

    invite.game = game
    invite.save()

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



