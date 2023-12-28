from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import never_cache

from rest_framework.decorators import api_view

from .models import User
from django.http import HttpResponse

import jwt
import requests

@never_cache
def login(request):

    """
    This view is used to render the login page.
    """

    # Check if 42 login is enabled
    context = {
       'LOGIN_42': settings.LOGIN_42, 
       'LOGIN_URL': settings.LOGIN_URL,
        'PATH': 'login',
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'login.html', context)
    else:
        return render(request, '../templates/base.html', context)

@never_cache
def register(request):
    """
    This view is used to render the register page.
    """
    # if User.objects.filter(username='test').count() == 0:
    #     new_user = User.objects.create(username='test')
    # return HttpResponse(User.objects.values_list('username'))
    context = {
       'LOGIN_URL': settings.LOGIN_URL,
        'PATH': 'register'
    }
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
    context = {
        'PATH': 'home'
    }
    # remove bearer from auth
    auth = request.headers.get('Authorization')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if auth is not None and request.user.is_authenticated:
            user_response = requests.get(settings.USER_URL + "/profile/", headers={'Authorization': auth})

            print(user_response.json())

            response = render(request, 'homeUser.html', context)
        else:
            response = render(request, 'home.html', context)
    else:
        response = render(request, '../templates/base.html', context)
    return response
