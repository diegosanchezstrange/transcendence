from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request, *args, **kwargs):

    user = request.user
    return JsonResponse({
        "username": user.username,
    })
