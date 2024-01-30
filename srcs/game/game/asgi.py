"""
ASGI config for game project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.urls import path
import sys
sys.path.append('../game_sockets')
from game_sockets.consumers import GameConsumer, ClientConsumer

#from game_sockets.urls import urlpatterns as websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game.settings')

# application = get_asgi_application()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter([path('ws/game/<str:room>/', ClientConsumer.as_asgi())]))),
         "channel": ChannelNameRouter({"game_engine": GameConsumer.as_asgi()}),
    }
)