from django.urls import path
from .views import create_user, login_oauth, validate_jwt

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .utils.CustomTokenObtainPairView import CustomTokenObtainPairView


urlpatterns = [
    path('register/', create_user),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/42/', login_oauth),
    path('validate/', validate_jwt),
]
