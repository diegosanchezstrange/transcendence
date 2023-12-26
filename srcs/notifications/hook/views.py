from django.http import JsonResponse
from functools import wraps
from notifications.settings import MICROSERVICE_API_TOKEN
from rest_framework.decorators import api_view


# TODO: get from commons
def private_microservice_endpoint(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        api_token = request.headers.get('Authorization')
        if not api_token or api_token != MICROSERVICE_API_TOKEN:
            return JsonResponse({'detail': 'Invalid API token.'}, status=401)
        return f(request, *args, **kwargs)
    return decorated_function


@api_view(['POST'])
@private_microservice_endpoint
def notification_hook(request, *args, **kwargs):
    message = dict(request.data)
    print(message)
    return JsonResponse({
        "detail": message
    })
