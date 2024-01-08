from django.shortcuts import render
from django.views.decorators.cache import never_cache

@never_cache
def base(request):
    response = render(request, 'base.html')
    return response
