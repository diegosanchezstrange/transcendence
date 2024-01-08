from django.urls import path
from .views import friends_list, send_friend_request, friend_requests_list, accept_friend_request

urlpatterns = [
    path('', friends_list),
    path('requests/send/', send_friend_request),
    path('requests/accept/', accept_friend_request),
    path('requests/', friend_requests_list),
]
