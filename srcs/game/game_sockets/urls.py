from . import consumers
from django.urls import path
    
urlpatterns = [
    # path('ws/game/<str:room>/', consumers.ClientConsumer.as_asgi()),
    path('ws/game/', consumers.ClientConsumer.as_asgi()),
]
