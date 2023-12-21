from django.urls import path
from .views import profile_view, change_user_data

urlpatterns = [
    path('profile/', profile_view),
    path('profile/change/', change_user_data),
]