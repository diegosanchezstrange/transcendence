from django.shortcuts import render
from django.conf import settings
from .models import User 
from django.http import HttpResponse

def base(request):
    return render(request, 'base.html')

def login(request):
    # Check if 42 login is enabled
    #context = {
    #    'LOGIN_42': settings.LOGIN_42, 
    #    'AUTH_URL': settings.AUTH_URL
    #}
    return render(request, 'partials/login.html')

def register(request): # this is a mock to test the database
    if User.objects.filter(username='test').count() == 0:
        new_user = User.objects.create(username='test')
    return HttpResponse(User.objects.values_list('username'))

def home(request):
    return render(request, 'partials/home.html')
