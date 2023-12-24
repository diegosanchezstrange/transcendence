from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import UserProfile
from functools import wraps
from src.settings import MICROSERVICE_API_TOKEN


# Private endpoint decorator
# TODO: put in common lib
def private_microservice_endpoint(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        api_token = request.headers.get('Authorization')
        if not api_token or api_token != MICROSERVICE_API_TOKEN:
            return JsonResponse({'detail': 'Invalid API token.'}, status=401)
        return f(request, *args, **kwargs)
    return decorated_function


# TODO: only for dev purposes, delete in prod
@api_view(['DELETE'])
def dev_view_delete_user(request, *args, **kwargs):
    username = request.data.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({
            "detail": "User not found."
        }, status=404)
    user.delete()
    return JsonResponse({
        "detail": f"User '{username}' was successfully deleted."
    }, status=200)


# TODO: delete this endpoint
@api_view(['GET'])
def dev_view_list_users(request, *args, **kwargs):
    users = User.objects.all()
    usernames = [{
        "user_id": user.id,
        "username": user.username,
        "login": user.userprofile.login
    } for user in users]

    return JsonResponse({
        "detail": usernames
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_username(request, username, *args, **kwargs):
    user = get_object_or_404(User, username=username)
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "login": user.userprofile.login
    })


@api_view(['POST'])
@private_microservice_endpoint
def create_user(request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.create_user(username=username, password=password)
    user.save()

    return JsonResponse({
        "detail": "User created successfully",
        "data": {
            "id": user.id,
            "username": username
        }
    }, status=201)


@api_view(['POST'])
@private_microservice_endpoint
def get_or_create_user_oauth(request, *args, **kwargs):
    login = request.data.get('username')

    try:
        user = UserProfile.objects.get(login=login).user
        return JsonResponse({
            "detail": "User found successfully",
            "user_id": user.id
        }, status=200)

    except UserProfile.DoesNotExist:
        username = login
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username)
            user.set_unusable_password()
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.login = login
            profile.save()
            return JsonResponse({
                "detail": "User created successfully",
                "user_id": user.id
            }, status=201)

        suffix = 2
        while User.objects.filter(username=f'{username}{suffix}').exists():
            suffix += 1

        user = User.objects.create_user(username=f'{username}{suffix}')
        user.set_unusable_password()
        profile = UserProfile.objects.get(user=user)
        profile.login = login
        profile.save()

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
    }, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request, *args, **kwargs):
    user = request.user
    UserProfile.objects.get_or_create(user=user)

    return JsonResponse({
        "detail": {
            "id": user.id,
            "username": user.username,
            "login": user.userprofile.login,
        }
    })
