from django.conf import settings
from .Queue import Queue
from .Tournament import Tournament as Tourna
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from game.game_matchmaking.models import UserTournament, Tournament
import requests 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_queue(request, *args, **kwargs):
    user = request.user

    if Queue.is_user_in_queue(user):
        return JsonResponse({
            "message": "You are already in a queue."
        }, status=403)

    try:
        Queue.add_player(user)
    except Exception as e:
        print(e)
        return JsonResponse({
            "message": "Error while joining the queue."
        }, status=500)

    return JsonResponse({
        "message": "Queue joined successfully."
    }, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_queue(request, *args, **kwargs):
    user = request.user

    try:
        Queue.leave_queue(user)
    except Queue.UserNotInQueueError:
        return JsonResponse({
            "message": "You are not in a queue currently."
        }, status=403)

    return JsonResponse({
        "message": "Queue left successfully."
    }, status=200)


# TODO: delete this view and the one below
@api_view(['GET'])
def dev_view_get_queue(request, *args, **kwargs):
    queue_raw = Queue.get_queue()

    queue_usernames = [user.username for user in queue_raw]

    return JsonResponse({
        "detail": queue_usernames
    })

@api_view(['DELETE'])
def dev_view_delete_queue(request, *args, **kwargs):
    Queue.delete_queue()
    return JsonResponse({"message": "Queue deleted."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_tournament(request, *args, **kwargs):
    user = request.user

    id = User.objects.get(id=user['id'])
    hasTournament = UserTournament.objects.filter(user=user,
        tournament__tournament_winner=None, tournament__status__in=[Tournament.TournamentStatus.WAITING, Tournament.TournamentStatus.IN_PROGRESS]).exists()
    if hasTournament:
        return JsonResponse({'error': 'user already in a tournament'}, status=409)
 
    # if Tourna.is_user_in_queue(user):
    #     return JsonResponse({
    #         "message": "You are already in a queue."
    #     }, status=403)

    try:
        Tourna.add_player(user)
        return JsonResponse({
            "message": "Tournament joined successfully."
        }, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({
         "message": "Error while joining the queue."
         }, status=500)

@api_view(['GET'])
def get_tournament_info(request, *args, **kwargs):
    tournmanet_id = request.GET.get('id')

    if tournmanet_id is None:
        return JsonResponse({
            "message": "Tournament ID is required."
        }, status=400)
    
    try:
        tournament = requests.get(f"{settings.GAME_SERVICE_HOST_INTERNAL}/tournament/{tournmanet_id}")
        return JsonResponse(tournament.json())
    except Exception as e:
        return JsonResponse({
            "message": "Tournament does not exist."
        }, status=404) 

@api_view(['GET'])
def get_tournamet_matches(request, *args, **kwargs):
    tournmanet_id = request.GET.get('id')

    if tournmanet_id is None:
        return JsonResponse({
            "message": "Tournament ID is required."
        }, status=400)
    
    try:
        matches = requests.get(f"{settings.GAME_SERVICE_HOST_INTERNAL}/tournament/{tournmanet_id}/matches")

        return JsonResponse(matches.json())
    except Exception as e:
        return JsonResponse({
            "message": "Matches not found."
        }, status=404)
