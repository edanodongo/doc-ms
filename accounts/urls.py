from django.urls import path
# from . import views
# from accounts.views import RegisterView, ProfileView, ChangePasswordView, PasswordResetRequestView, PasswordResetConfirmView
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    # For user registration and authentication
    path('register/', views.RegisterView, name='register'),
    path('login/', views.TokenObtainPairView, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # For users to view profile 
    path('profile/', views.ProfileView, name='profile'),

    # For users to log out
    path('logout/', views.TokenBlacklistView, name='token_blacklist'),

    # For users to change their password
    path('change-password/', views.ChangePasswordView, name='change_password'),

    # For password reset functionality
    path('password-reset/request/', views.PasswordResetRequestView, name='password_reset_request'),
    path('password-reset/confirm/', views.PasswordResetConfirmView, name='password_reset_confirm'),
]




