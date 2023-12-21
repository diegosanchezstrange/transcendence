from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import never_cache

from .models import User 
from django.http import HttpResponse

@never_cache
def base(request):
    response = render(request, 'base.html')
    return response

@never_cache
def login(request):
    # Check if 42 login is enabled
    context = {
       'LOGIN_42': settings.LOGIN_42, 
       'LOGIN_URL': settings.LOGIN_URL,
        'PATH': 'login',
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/login.html', context)
    else:
        return render(request, 'base.html', context)

@never_cache
def register(request): # this is a mock to test the database
    # if User.objects.filter(username='test').count() == 0:
    #     new_user = User.objects.create(username='test')
    # return HttpResponse(User.objects.values_list('username'))
    context = {
        'PATH': 'register'
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/register.html', context)
    else:
        return render(request, 'base.html', context)

@never_cache
def home(request):
    # Check if req is from the browser or an ajax call
    context = {
        'PATH': 'home'
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        response = render(request, 'partials/home.html', context)
    else:
        response = render(request, 'base.html', context)
    return response
