from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from .models import UserProfile
from functools import wraps
from src.settings import MICROSERVICE_API_TOKEN
from django.shortcuts import get_object_or_404, redirect
from .models import FriendRequest, Friendship
from django.db.models import Q


# Private endpoint decorator
# TODO: put in tcommons
def api_token_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        api_token = request.headers.get('Authorization')
        if not api_token or api_token != MICROSERVICE_API_TOKEN:
            return JsonResponse({'detail': 'Invalid API token.'}, status=401)
        return f(request, *args, **kwargs)
    return decorated_function


@api_view(['POST'])
@api_token_required
def create_user(request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.create_user(username=username, password=password)
    user.save()

    profile, created = UserProfile.objects.get_or_create(user=user)

    return JsonResponse({
        "detail": "User created successfully"
    }, status=201)


@api_view(['POST'])
@api_token_required
def create_user_oauth(request, *args, **kwargs):
    username = request.data.get('username')

    user = User.objects.create_user(username=username)
    user.save()

    profile, created = UserProfile.objects.get_or_create(user=user)

    return JsonResponse({
        "detail": "User created successfully",
        "user_id": user.id
    }, status=201)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_user_data(request, *args, **kwargs):
    test = request.data.get('test') or request.user.userprofile.test
    username = request.data.get('username') or request.user.username

    if not test and not username:
        return JsonResponse({
            "detail": "No value provided"
        }, status=304)
    
    user = request.user

    request.user.userprofile.test = test
    request.user.username = username
    user.save()

    return JsonResponse({
        "detail": "User updated successfully"
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request, *args, **kwargs):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    return JsonResponse({
        "detail": {
            "username": user.username,
            "user_id": user.id,
            "profile": profile.test
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, *args, **kwargs):
    send_to = request.data.get('send_to')
    if not send_to:
        return JsonResponse({
            "detail": "No value provided"
        }, status=400)

    receiver = User.objects.get(username=send_to)

    if not receiver:
        return JsonResponse({
            "detail": "User does not exist"
        }, status=404)

    friend_request, created = FriendRequest.objects.get_or_create(
        sender=request.user,
        receiver=receiver
    )
    if created:
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

    friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)

    if not friend_request:
        return JsonResponse({
            "detail": "Friend request does not exist"
        }, status=404)

    friend_request.delete()
    Friendship.objects.create(user1=request.user, user2=friend_request.sender)

    return JsonResponse({
        "detail": "OK"
    }, status=201)


