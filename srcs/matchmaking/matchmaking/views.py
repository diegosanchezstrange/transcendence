from django.conf import settings
from .Queue import Queue
from .Tournament import Tournament as Tourna
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import requests 

from functools import wraps

def private_or_public_endpoint(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return f(request, *args, **kwargs)
        
        api_token = request.headers.get('Authorization')
        if not api_token or api_token != settings.MICROSERVICE_API_TOKEN:
            return JsonResponse({'detail': 'Invalid API token.'}, status=401)
        return f(request, *args, **kwargs)
    return decorated_function

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
@private_or_public_endpoint
#@authentication_classes([])
@permission_classes([])
def leave_queue(request, *args, **kwargs):

    if request.user.is_authenticated:
        user = request.user
    else:
        user_id = request.data.get('user_id')
        if user_id is None:
            return JsonResponse({
                "message": "User ID is required."
            }, status=400)
        user = User.objects.get(pk=user_id)

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

    if Tourna.is_user_in_queue(user):
        return JsonResponse({
            "message": "You are already in a queue."
        }, status=403)

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

@api_view(['POST'])
@private_or_public_endpoint
#@authentication_classes([])
@permission_classes([])
def leave_tournament(request, *args, **kwargs):
    if request.user.is_authenticated:
        user = request.user
    else:
        user_id = request.data.get('user_id')
        if user_id is None:
            return JsonResponse({
                "message": "User ID is required."
            }, status=400)
        user = User.objects.get(pk=user_id)

    try:
        Tourna.leave_queue(user)
    except Tourna.UserNotInQueueError:
        return JsonResponse({
            "message": "You are not in a queue currently."
        }, status=403)

    return JsonResponse({
        "message": "Tournament left successfully."
    }, status=200)

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
