from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import UserProfile
from functools import wraps
from src.settings import MICROSERVICE_API_TOKEN
from django.core.files.storage import default_storage
import os
from src import settings


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
        "login": user.userprofile.login,
        "profile_pic": f'{request.scheme}://{request.get_host()}{user.userprofile.profile_pic.url}'
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
        "login": user.userprofile.login,
        "profile_pic": f'{request.scheme}://{request.get_host()}{user.userprofile.profile_pic.url}'
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
def change_user_name(request, *args, **kwargs):
    username = request.data.get('username') or request.user.username

    if not username:
        return JsonResponse({
            "detail": "No value provided"
        }, status=304)
    
    user = request.user

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
            "profile_pic": f'{request.scheme}://{request.get_host()}{user.userprofile.profile_pic.url}'
        }
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def upload_profile_picture(request, *args, **kwargs):
    profile_pic = request.FILES.get('profile_pic')

    if not profile_pic:
        return JsonResponse({
            "detail": "No profile picture provided"
        }, status=400)

    profile = request.user.userprofile
    username = request.user.username

    file_extension = os.path.splitext(profile_pic.name)[1]
    if file_extension[1:] not in ('jpg', 'jpeg', 'png'):
        return JsonResponse({
            "detail": "Invalid file format. (must be jpg, jpeg or png)."
        }, status=400)

    status_code = 201
    save_to = f'{settings.MEDIA_ROOT}/{username}{file_extension}'

    if default_storage.exists(save_to):
        default_storage.delete(save_to)
        status_code = 200

    path = default_storage.save(save_to, profile_pic)
    profile.profile_pic = path
    profile.save()
    return JsonResponse({
        "detail": "Profile pic uploaded.",
        "url": profile.profile_pic.url
    }, status=status_code)

