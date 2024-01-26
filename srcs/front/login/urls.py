from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login/auth42/', views.login_42, name='login43'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
]
