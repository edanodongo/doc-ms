from django.shortcuts import render
 # This file contains the views for user registration, login, and profile management
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
 
# Serializer for user registration
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
# View for user profile
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

#  To allow users to change their password
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Wrong password.'}, status=400)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Password updated.'})
        return Response(serializer.errors, status=400)

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.conf import settings

# Serializer for password reset request
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_user_model().objects.filter(email=email).first()
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/reset-password/?uid={uid}&token={token}"

            send_mail(
                "Password Reset Request",
                f"Reset your password: {reset_url}",
                "noreply@docms.com",
                [user.email],
            )
        return Response({"detail": "If your account exists, a password reset link has been sent."})
