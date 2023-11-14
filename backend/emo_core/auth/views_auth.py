from django.utils import timezone
from django.db import transaction
from rest_framework import status, views
from rest_framework.response import Response
from ..serializers import UserModelSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers_auth import CustomTokenObtainPairSerializer
from ..models import TempRegisterToken, TemporaryCode, UserModel
from rest_framework.decorators import permission_classes
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from ..line_bot.line_bot_api import send_temporary_code
from django.utils import timezone
from datetime import timedelta



class RegisterView(views.APIView):
    def post(self, request):
        # Validate token
        token = request.data.get('token')
        temp_record = TempRegisterToken.objects.filter(token=token).first()
        
        # トークンの存在と有効性のチェック
        if not temp_record or temp_record.is_expired():
            print("Invalid or expired token")
            user = UserModel.objects.filter(line_user_id=str(temp_record)).first()
            user.delete()
            temp_record.delete()
            return Response({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            serializer = UserModelSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.line_user_id = str(temp_record)
                
                if UserModel.objects.filter(line_user_id=user.line_user_id).exists():
                    # check the user name whose line_user_id is the same as the new user's line_user_id
                    existing_user = UserModel.objects.get(line_user_id=user.line_user_id)
                    existing_user.delete()
                user.save()
                
                # Create user profile
                profile_data = request.data.copy()
                profile_serializer = UserProfileSerializer(data=profile_data)
                temp_record.delete()
                
                if profile_serializer.is_valid():
                    # Assign the user object to the profile and save
                    profile = profile_serializer.save(user=user)
                else:
                    print("Invalid profile data")
                    return Response({"message": "Invalid profile data"}, status=status.HTTP_400_BAD_REQUEST)
                
                print("User created successfully")
                return Response(status=status.HTTP_201_CREATED)
            else:
                print("Already exists")
                return Response({"message": "A User with that user name already exists"}, status=status.HTTP_400_BAD_REQUEST)

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
    

@permission_classes([IsAuthenticated])
class SendTemporaryCode(views.APIView):
    def post(self, request, *args, **kwargs):
        user = request.user

        try:
            if not user.line_user_id:
                return Response({"error": "LINE user ID not found."}, status=status.HTTP_404_NOT_FOUND)

            temp_code = send_temporary_code(user.line_user_id)
            expiration_time = timezone.now() + timedelta(minutes=3)  # 例: 3分後に期限切れ

            TemporaryCode.objects.create(
                user=user,
                code=temp_code,
                expiration=expiration_time
            )

            return Response({"message": "Temporary code sent to LINE user."}, status=status.HTTP_200_OK)

        except UserModel.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

