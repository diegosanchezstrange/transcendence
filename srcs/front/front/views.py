from django.shortcuts import render
from django.views.decorators.cache import never_cache

@never_cache
def base(request, context):
    response = render(request, 'base.html', context)
    return response
