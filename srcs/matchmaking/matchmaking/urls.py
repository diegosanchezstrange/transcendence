"""
URL configuration for matchmaking project.

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
from django.urls import path
from .views import join_queue, dev_view_get_queue, leave_queue, join_tournament, get_tournament_info


urlpatterns = [
    path('admin/', admin.site.urls),
    path('queue/join/', join_queue),
    path('queue/leave/', leave_queue),
    path('queue/list/', dev_view_get_queue),
    path('queue/delete/', dev_view_get_queue),
    path('tournament/join/', join_tournament),
    path('tournament/info/', get_tournament_info)

]
