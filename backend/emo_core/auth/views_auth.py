from django.contrib.auth import authenticate
from rest_framework import status, views
from rest_framework.response import Response
from .serializers_auth import LoginSerializer
from ..serializers import UserModelSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import TempRegister

class RegisterView(views.APIView):
    def post(self, request):
        # validate token
        token = request.data.get('token')
        temp_record = TempRegister.objects.filter(token=token).first()
        if not temp_record:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        # create user
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.line_user_id = temp_record.line_user_id
            user.save()
            
            # create user profile
            profile = UserProfileSerializer(data=request.data)
            if profile.is_valid():
                profile.save(user=user)
            else:
                return Response(profile.errors, status=status.HTTP_400_BAD_REQUEST)

            # Delete the temp_record as it's no longer needed
            temp_record.delete()

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

