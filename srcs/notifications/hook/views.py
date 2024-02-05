from django.http import JsonResponse
from functools import wraps
from notifications.settings import MICROSERVICE_API_TOKEN
from rest_framework.decorators import api_view
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
    message: dict = dict(request.data)

    user_id = message['receiver']['id']
    group_name = f'group_{user_id}'

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_message",
            "ntype": message["ntype"],
            "message": message['message'],
        }
    )
    return JsonResponse({
        "detail": "OK"
    })
