from django.urls import path
from .views import reject_friend_request, send_friend_request, friend_requests_list, accept_friend_request, reject_friend_request
from .views import FriendView

urlpatterns = [
    path('', FriendView.as_view()),
    path('<int:id>/', FriendView.as_view()),
    path('requests/send/', send_friend_request),
    path('requests/accept/', accept_friend_request),
    path('requests/reject/', reject_friend_request),
    path('requests/', friend_requests_list),
]
