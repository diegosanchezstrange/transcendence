from django.urls import path
from .views import notification_hook

urlpatterns = [
    path('send/', notification_hook, name='hook')
]
