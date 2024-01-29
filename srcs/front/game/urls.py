from django.urls import path
from . import views

urlpatterns = [
    path('pong/', views.start),
    path('lobby/', views.lobby),
]