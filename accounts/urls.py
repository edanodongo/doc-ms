from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    # For user registration and authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # For users to view profile 
    path('profile/', ProfileView.as_view(), name='profile'),

    # For users to log out
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # For users to change their password
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]




