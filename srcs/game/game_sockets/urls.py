from . import consumers
from django.urls import path
    
urlpatterns = [
    path('ws/game/', consumers.LobbyConsumer.as_asgi()),
]