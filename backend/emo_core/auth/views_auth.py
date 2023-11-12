from django.utils import timezone
from django.db import transaction
from rest_framework import status, views
from rest_framework.response import Response
from ..serializers import UserModelSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers_auth import CustomTokenObtainPairSerializer
from ..models import TempRegister

from django.conf import settings
from rest_framework.permissions import IsAuthenticated



class RegisterView(views.APIView):
    def post(self, request):
        # Validate token
        token = request.data.get('token')
        temp_record = TempRegister.objects.filter(token=token).first()
        
        # トークンの存在と有効性のチェック
        if not temp_record or temp_record.expiry_date < timezone.now():
            return Response({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            serializer = UserModelSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.line_user_id = temp_record.line_user_id
                user.save()
                
                # Create user profile
                profile_data = request.data.copy()
                profile_serializer = UserProfileSerializer(data=profile_data)
                if profile_serializer.is_valid():
                    # Assign the user object to the profile and save
                    profile = profile_serializer.save(user=user)
                else:
                    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Delete the temp_record as it's no longer needed
                temp_record.delete()

                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errorsw, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            secure_cookie = settings.SESSION_COOKIE_SECURE
            samesite_cookie = settings.SESSION_COOKIE_SAMESITE if hasattr(settings, 'SESSION_COOKIE_SAMESITE') else 'Lax'
            httponly_cookie = settings.SESSION_COOKIE_HTTPONLY

            response.set_cookie(
                'access',
                data['access'],
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                httponly=httponly_cookie,
                samesite=samesite_cookie,
                secure=secure_cookie
            )
            response.set_cookie(
                'refresh',
                data['refresh'],
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                httponly=httponly_cookie,
                samesite=samesite_cookie,
                secure=secure_cookie
            )
            return response
        return response
    
class CustomRefreshTokenView(views.APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token is None:
            return Response({"detail": "Refresh token not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 既存のリフレッシュトークンで新しいアクセストークンを生成
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            # 新しいアクセストークンをCookieにセット
            response = Response()
            response.set_cookie(
                'access',
                new_access_token,
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                httponly=True,
                samesite='Strict',
                secure=settings.SESSION_COOKIE_SECURE
            )
            return response

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = Response({"Message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response

