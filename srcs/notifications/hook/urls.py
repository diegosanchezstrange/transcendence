from django.urls import path
from views import notification_hook

urlpatterns = [
    path('', notification_hook, name='hook')
]
