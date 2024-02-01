from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import never_cache

from rest_framework.decorators import api_view

from .models import User
from django.http import HttpResponse

import jwt
import requests

context = {
    'LOGIN_SERVICE_HOST': settings.LOGIN_SERVICE_HOST,
    'USERS_SERVICE_HOST': settings.USERS_SERVICE_HOST,
    'NOTIFICATIONS_SERVICE_HOST': settings.NOTIFICATIONS_SERVICE_HOST,
    'NOTIFICATIONS_SOCKETS_HOST': settings.NOTIFICATIONS_SOCKETS_HOST,
    'GAME_SOCKETS_HOST': settings.GAME_SOCKETS_HOST,
}

@never_cache
def login(request):

    """
    This view is used to render the login page.
    """

    context['PATH'] = 'login'
    context['LOGIN_42_URL'] = settings.LOGIN_42_URL
    if settings.LOGIN_42:
        context['LOGIN_42'] = settings.LOGIN_42
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'login.html', context)
    else:
        return render(request, '../templates/base.html', context)

@never_cache
def login_42(request):
    """
    This view is used to render the login page.
    """
    context['PATH'] = 'home'

    # Get a parameter from the request
    code = request.GET.get('code')

    if code is None:
        return HttpResponse('No code provided')
    
    token = requests.post(settings.LOGIN_SERVICE_HOST + "/auth/login/42/",
                          data={'code': code})
    print(token.json())
    if token.status_code != 200:
        return HttpResponse("Invalid code")

    response = render(request, '../templates/base.html', context)
    response.set_cookie('token', token.json()['token'])

    return response

@never_cache
def register(request):
    """
    This view is used to render the register page.
    """
    # if User.objects.filter(username='test').count() == 0:
    #     new_user = User.objects.create(username='test')
    # return HttpResponse(User.objects.values_list('username'))
    context['PATH'] = 'register'
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'register.html', context)
    else:
        return render(request, '../templates/base.html', context)

@never_cache
@api_view(['GET'])
def home(request):
    """
    This view is used to render the home page.
    """
    # Check if req is from the browser or an ajax call
    context['PATH'] = 'home'
    # remove bearer from auth
    auth = request.headers.get('Authorization')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if auth is not None and request.user.is_authenticated:
            user_response = requests.get(settings.USERS_SERVICE_HOST_INTERNAL + "/profile/", headers={'Authorization': auth}, verify=False)
            context['user_info'] = user_response.json()['detail']
            response = render(request, 'homeUser.html', context)
        else:
            response = render(request, 'home.html', context)
    else:
        response = render(request, '../templates/base.html', context)
    return response
