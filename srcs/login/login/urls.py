from django.urls import path
from . import views

urlpatterns = [
    path('login/' , views.Login.as_view()),
    path('register/', views.register),
    path('validate/', views.validate),
]
