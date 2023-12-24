from django.urls import path
from .views import create_user, dev_view_list_users, get_or_create_user_oauth, dev_view_delete_user
from .views import get_user_by_username

urlpatterns = [
    path('', dev_view_list_users),
    path('<str:username>/', get_user_by_username),
    path('create/', create_user),
    path('create/42/', get_or_create_user_oauth),
    path('delete/', dev_view_delete_user),
    # path('profile/change/', change_user_data),
]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('profile/', profile_view),
#     path('profile/change/', change_user_data),
#     path('user/create/', create_user),
#     path('users/', dev_view_list_users),
#     path('user/delete/', dev_view_delete_user),
#     path('user/create/42/', create_user_oauth),
