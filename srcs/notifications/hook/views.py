from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def notification_hook(request, *args, **kwargs):
    return JsonResponse({
        "detail": "OK"
    })
