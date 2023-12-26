from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from .models import Friendship, FriendRequest
from .notifications.send_notification import send_friend_request_notification
from .notifications.constants import NotificationType
from .utils.utils import is_your_friend
from django.shortcuts import get_object_or_404


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, *args, **kwargs):
    send_to = request.data.get('send_to')
    if not send_to:
        return JsonResponse({
            "detail": "No value provided"
        }, status=400)

    receiver = get_object_or_404(User, username=send_to)

    if is_your_friend(request.user, receiver):
        return JsonResponse({
            "detail": f"You are already a friend of {receiver.username}."
        }, status=200)

    friend_request, created = FriendRequest.objects.get_or_create(
        sender=request.user,
        receiver=receiver
    )
    if created:
        send_friend_request_notification(request.user, receiver, NotificationType.SENT)

        return JsonResponse({
            "detail": "Friend request sent successfully"
        }, status=201)
    else:
        # TODO: send 304 (postman bug)
        return JsonResponse({
            "detail": "Friend request already sent."
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_requests_list(request):
    friend_requests = FriendRequest.objects.filter(receiver=request.user)

    result = [friend_request.sender.username for friend_request in friend_requests if friend_request]

    return JsonResponse({
        "detail": result
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friends_list(request, *args, **kwargs):
    user = request.user
    friends = Friendship.objects.filter(Q(user1=user) | Q(user2=user))

    names = []
    for friend in friends:
        if friend.user1 == user:
            names.append(friend.user2.username)
        elif friend.user2 == user:
            names.append(friend.user1.username)

    return JsonResponse({
        "detail": names
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, *args, **kwargs):
    receiver = request.user
    sender_name = request.data.get("sender")
    sender = User.objects.get(username=sender_name)

    if not sender:
        return JsonResponse({
            "detail": "Sender does not exist"
        }, status=404)

    if not sender:
        return JsonResponse({}, status=400)

    friend_request = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)

    if not friend_request:
        return JsonResponse({
            "detail": "Friend request does not exist"
        }, status=404)

    friend_request.delete()
    Friendship.objects.create(user1=request.user, user2=friend_request.sender)

    return JsonResponse({
        "detail": "OK"
    }, status=201)
