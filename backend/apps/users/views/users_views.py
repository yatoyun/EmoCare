from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from rest_framework.permissions import IsAuthenticated

from apps.users.serializers.users_serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UpdateUserSerializer
)
from apps.users.services.users_services import (
    register_user,
    login_user
)

import logging

logger = logging.getLogger(__name__)

###
# Write HEALTH here because of the path.
###
class HealthView(APIView):
    def get(self, request):
        return Response({'detail': 'Health check passed'}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        logger.info(f"Registration attempt with email: {request.data.get('email')}")
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Registration validation failed: {serializer.errors}")
            return Response({
                'detail': 'Validation error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = register_user(**serializer.validated_data)
        except ValueError as e:
            logger.error(f"Registration failed: {str(e)}")
            return Response({
                'detail': str(e),
                'error_type': 'registration_error'
            }, status=status.HTTP_400_BAD_REQUEST)

        auth_login(request, user)
        logger.info(f"User registered successfully: {user.email}")
        return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        logger.info("Login attempt")
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Login validation failed: {serializer.errors}")
            return Response({
                'detail': 'Validation error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            name = serializer.validated_data.get('name')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = login_user(name=name, email=email, password=password)
            auth_login(request, user)
            logger.info(f"User logged in successfully: {user.email}")
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Login failed: {str(e)}")
            return Response({
                'detail': str(e),
                'error_type': 'authentication_error'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"User logged out: {request.user.email}")
        auth_logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

class UserView(APIView):
    """
    GET: ユーザー情報の取得
    PATCH: ユーザー情報の更新
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({
            'detail': 'User information retrieved successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = UpdateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.update(user, serializer.validated_data)
        updated_serializer = UserSerializer(user)
        return Response({
            'detail': 'User information updated successfully',
            'user': updated_serializer.data
        }, status=status.HTTP_200_OK)
