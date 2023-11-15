from django.shortcuts import render
from django.conf import settings

# Create your views here.

def base(request):
    return render(request, 'base.html')

def login(request):
    # Check if 42 login is enabled
    context = {
        'LOGIN_42': settings.LOGIN_42, 
        'AUTH_URL': settings.AUTH_URL
    }
    return render(request, 'partials/login.html', context)

def home(request):
    return render(request, 'partials/home.html')
