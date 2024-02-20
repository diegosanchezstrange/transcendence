from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view
from src import settings
import requests
import os
from .utils.utils import request_intra
from requests.exceptions import RequestException
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.state import token_backend


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

        if len(username) > 32:
            return JsonResponse({
                "status": 400,
                "message": "Username cannot be more than 32 characters"
            }, status=400)
        if len(password) > 32:
            return JsonResponse({
                "status": 400,
                "message": "Password cannot be more than 32 characters"
            }, status=400)

        body = {
            "username": username,
            "password": password
        }

        url = f"{settings.USERS_SERVICE_HOST}/users/create/"

        headers = {
            "Authorization": os.getenv('MICROSERVICE_API_TOKEN')
        }

        response = requests.post(url, data=body, headers=headers, verify=False)

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
    # Get 42 access token with the return code
    code = request.data.get('code')
    if not code:
        return JsonResponse({
            "detail": "Code missing."
        }, status=400)
    url = f"{settings.API_INTRA_URL}/oauth/token"
    body = {
        "grant_type": "authorization_code",
        "client_id": settings.LOGIN_42_CLIENT,
        "client_secret": settings.LOGIN_42_SECRET,
        "code": code,
        "redirect_uri": f"{settings.BASE_URL}/login/auth42/"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    access_token = requests.post(url, data=body, headers=headers)

    if access_token.status_code != 200:
        return JsonResponse({
            "detail": "Invalid code."
        }, status=400)

    access_token = access_token.json().get("access_token")


    # Get user info with the access token
    url = f"{settings.API_INTRA_URL}/v2/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = request_intra(url, headers)
    except RequestException:
        return JsonResponse({
            "detail": "Intra 42 Client Error."
        }, status=502)

    if response.status_code != 200:
        return JsonResponse({
            "detail": "Invalid access token."
        }, status=401)

    # Get or create user with the 42 username
    json_response = response.json()
    username = json_response.get("login")
    image_url = json_response['image']['versions']['large']
    headers = {
        "Authorization": settings.MICROSERVICE_API_TOKEN
    }
    body = {
        "username": username,
        "image_url": image_url
    }
    url = f"{settings.USERS_SERVICE_HOST}/users/create/42/"
    response = requests.post(url, headers=headers, data=body, verify=False)
    if response.status_code not in (200, 201):
        return JsonResponse({
            "detail": "Unable to get or create user."
        }, status=500)

    user_id = response.json().get('user_id')
    user = User.objects.get(pk=user_id)
    jwt_token = AccessToken.for_user(user)

    return JsonResponse({
        "token": str(jwt_token)
    })

@api_view(['POST'])
def validate_jwt(request, *args, **kwargs):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return JsonResponse({"message": "Invalid token"}, status=401)
    
    extract = auth_header.split()
    if len(extract != 2):
        return JsonResponse({"message": "Bad authorization header"}, status=400)

    token = extract[1]
    try:
        UntypedToken(token)
        token_backend.decode(token, verify=True)
        return JsonResponse({"message": "Valid JWT"}, status=200)
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"message": "Invalid JWT token."}, status=401)
