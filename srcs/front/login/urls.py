from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
]

