from .Queue import Queue
from .Tournament import Tournament as Tourna
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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

    if Tourna.is_user_in_queue(user):
        return JsonResponse({
            "message": "You are already in a queue."
        }, status=403)

    try:
        Tourna.add_player(user)
    except Exception as e:
        print(e)
        return JsonResponse({
            "message": "Error while joining the queue."
        }, status=500)

    
