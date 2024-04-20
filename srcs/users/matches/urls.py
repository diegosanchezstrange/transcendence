from django.urls import path
from .views import MatchView

urlpatterns = [
    path('', MatchView.as_view())
]
