from .Queue import Queue
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(['POST'])
def join_queue(request, *args, **kwargs):
    user_id = request.data.get('user_id')
    Queue.add_player(user_id)
    return JsonResponse({'success': True})
