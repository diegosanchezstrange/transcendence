from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from .models import UserProfile
from functools import wraps
from src.settings import MICROSERVICE_API_TOKEN

# Create your views here.


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
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_user_data(request, *args, **kwargs):
    new_value = request.data.get('test')
    
    if not new_value:
        return JsonResponse({
            "detail": "No value provided"
        }, status=304)
    
    user = request.user
    request.user.userprofile.test = new_value
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
            "profile": profile.test
        }
    })
