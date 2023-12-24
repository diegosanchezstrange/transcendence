from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view
from src import settings
import requests
import os


@api_view(['POST'])
def create_user(request, *args, **kwargs):
    """
    Create a user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.

        Example:
        {
            "status": 201,
            "message": "User 'username' created successfully."
        }

    Raises:
        JsonResponse: If the username or password is missing.
        JsonResponse: If the username already exists.
        JsonResponse: If the request method is not POST.

    Body:
        username (str): The username.
        password (str): The password.

    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return JsonResponse({
                "status": 400,
                "message": "Username or password missing."
            }, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": 409,
                "message": f"User with username '{username}' already exists."
            }, status=409)
        
        body = {
            "username": username,
            "password": password
        }

        # TODO: get hostname from env
        url = "http://localhost:8081/users/create/"

        headers = {
            "Authorization": os.getenv('MICROSERVICE_API_TOKEN')
        }
        
        response = requests.post(url, data=body, headers=headers)
        print(headers)
        if response.status_code != 201:
            raise Exception("bad")

        return JsonResponse({
            "status": 201,
            "message": f"User '{username}' created successfully."
        })

    return JsonResponse({
        "status": 405,
        "message": "User creation must be POST."
    }, status=405)


@api_view(['POST'])
def login_oauth(request, *args, **kwargs):
    access_token = request.data.get('access_token')
    # TODO: request in loop if request fails
    url = "https://api.intra.42.fr/v2/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return JsonResponse({
            "detail": "Invalid access token."
        }, status=401)

    username = response.json()["login"]
    headers = {
        "Authorization": settings.MICROSERVICE_API_TOKEN
    }
    body = {
        "username": username
    }
    url = "http://localhost:8081/users/create/42/"

    # TODO: get hostname from env
    response = requests.post(url, headers=headers, data=body)
    if response.status_code not in (200, 201):
        return JsonResponse({
            "detail": "error"
        })
    user_id = response.json()['user_id']
    user = User.objects.get(pk=user_id)
    jwt_token = AccessToken.for_user(user)

    return JsonResponse({
        "token": str(jwt_token)
    })
