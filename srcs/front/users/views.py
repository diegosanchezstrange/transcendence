from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.conf import settings
from django.views.decorators.cache import never_cache

from rest_framework.decorators import api_view

import requests
import jwt

# Create your views here.

@never_cache
@api_view(['GET'])
def profile(request):
    context = {
        'PATH': 'profile',
        'USERS_SERVICE_HOST': settings.USERS_SERVICE_HOST,
    }

    print(context)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            auth = request.headers.get('Authorization')
            user_response = requests.get(settings.USERS_SERVICE_HOST + "/profile/", headers={'Authorization': auth})
            context['user_info'] = user_response.json()['detail']

            return render(request, 'userProfile.html', context)
        else:
            # Redirect to login page with a 302 status
            return redirect("/login/")
    else:
        return render(request, 'base.html', context)
        
        
        
        