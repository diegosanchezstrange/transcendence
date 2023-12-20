from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


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

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return JsonResponse({
            "status": 201,
            "message": f"User '{username}' created successfully."
        })

    return JsonResponse({
        "status": 405,
        "message": "User creation must be POST."
    }, status=405)
