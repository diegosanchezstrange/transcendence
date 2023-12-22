"""
URL configuration for users project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import profile_view, create_user, change_user_data
from users.views import send_friend_request, friend_requests_list, accept_friend_request, friends_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', profile_view),
    path('profile/change/', change_user_data),
    path('user/create/', create_user),
    path('friends/request/', send_friend_request),
    path('friends/request/list/', friend_requests_list),
    path('friends/request/accept/', accept_friend_request),
    path('friends/list/', friends_list),
    # path('/', include('users.urls')),
]
