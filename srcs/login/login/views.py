from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from login.models import

from tcommons.jwt import JWT

import json


# Create your views here.

class Login(View):
    def post(self, request):
        print(request.body)
        jwt = JWT({"name": "Diego", "lastname": "Sanchez"})
        data = json.loads(request.body)
        if data['username'] == 'admin' and data['password'] == 'admin':
            response = {}
            response['success'] = True
            response['message'] = 'Login successful'
            response['token'] = '1234567890'
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            response = {}
            response['success'] = False
            response['message'] = 'Login failed'
            return HttpResponse(json.dumps(response),
                                content_type='application/json', status=403)


def register(request):
    return render(request, 'newUser.json')


def validate(request):
    return render(request, 'validate.json')
