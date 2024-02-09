from django.urls import path
from .views import create_user, dev_view_list_users, get_or_create_user_oauth, dev_view_delete_user
from .views import get_user_by_username, upload_profile_picture

urlpatterns = [
    path('', dev_view_list_users),
    path('create/', create_user),
    path('create/42/', get_or_create_user_oauth),
    path('delete/', dev_view_delete_user),
    path('upload/', upload_profile_picture),
]
