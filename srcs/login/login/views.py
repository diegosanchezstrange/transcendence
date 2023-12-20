from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_user(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

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
