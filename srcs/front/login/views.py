from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
def base(request):
    response = render(request, 'base.html')
    return response

def login(request):
    # Check if 42 login is enabled
    context = {
        'LOGIN_42': settings.LOGIN_42, 
        'AUTH_URL': settings.AUTH_URL
    }
    return render(request, 'partials/login.html', context)

@never_cache
def home(request):
    # Check if req is from the browser or an ajax call
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        response = render(request, 'partials/home.html')
    else:
        response = render(request, 'base.html')
    return response
