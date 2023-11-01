from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserModel, UserProfile, EmotionData, ChatLogs, AdviceData
from django.db.models import Avg, Max, Min, Count
from .serializers import UserModelSerializer, UserProfileSerializer, EmotionDataSerializer, ChatLogsSerializer, AdviceDataSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

    @action(detail=True, methods=['PATCH'])
    def update_user(self, request, pk=None):
        user = self.get_object()
        if user:
            # 既存のデータを取得
            serializer = UserModelSerializer(user, data=request.data, partial=True)  # partial=True で部分更新を許可
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "User updated", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['DELETE'])
    def delete_user(self, request, pk=None):
        user = self.get_object()
        if user:
            user.delete()
            return Response({"status": "User deleted"}, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmotionDataViewSet(viewsets.ModelViewSet):
    queryset = EmotionData.objects.all()
    serializer_class = EmotionDataSerializer

class ChatLogsViewSet(viewsets.ModelViewSet):
    queryset = ChatLogs.objects.all()
    serializer_class = ChatLogsSerializer

class AdviceDataViewSet(viewsets.ModelViewSet):
    queryset = AdviceData.objects.all()
    serializer_class = AdviceDataSerializer

class StatisticsView(viewsets.ViewSet):
    def list(self, request):
        # Average emotion score and magnitude
        avg_emotion_score = EmotionData.objects.all().aggregate(Avg('emotion_score'))['emotion_score__avg']
        avg_emotion_magnitude = EmotionData.objects.all().aggregate(Avg('emotion_magnitude'))['emotion_magnitude__avg']
        
        # Count of positive, negative, and neutral emotion entries
        count_positive = EmotionData.objects.filter(emotion_score__gt=0.2).count()
        count_negative = EmotionData.objects.filter(emotion_score__lt=-0.2).count()
        count_neutral = EmotionData.objects.filter(emotion_score__gte=-0.2, emotion_score__lte=0.2).count()

        # Mixed emotions: high magnitude but near-zero score
        count_mixed = EmotionData.objects.filter(emotion_score__gte=-0.2, emotion_score__lte=0.2, emotion_magnitude__gt=0.5).count()

        # Total chats and advices
        total_chats = ChatLogs.objects.count()
        total_advices = AdviceData.objects.count()

        stats = {
            'avg_emotion_score': avg_emotion_score,
            'avg_emotion_magnitude': avg_emotion_magnitude,
            'count_positive': count_positive,
            'count_negative': count_negative,
            'count_neutral': count_neutral,
            'count_mixed': count_mixed,
            'total_chats': total_chats,
            'total_advices': total_advices
        }
        return Response(stats)

    def retrieve(self, request, pk=None):
        # Filter by user
        user_emotion_data = EmotionData.objects.filter(user_id=pk)

        # Average emotion score and magnitude for this user
        avg_emotion_score = user_emotion_data.aggregate(Avg('emotion_score'))['emotion_score__avg']
        avg_emotion_magnitude = user_emotion_data.aggregate(Avg('emotion_magnitude'))['emotion_magnitude__avg']
        
        # Count of positive, negative, and neutral emotion entries for this user
        count_positive = user_emotion_data.filter(emotion_score__gt=0.2).count()
        count_negative = user_emotion_data.filter(emotion_score__lt=-0.2).count()
        count_neutral = user_emotion_data.filter(emotion_score__gte=-0.2, emotion_score__lte=0.2).count()

        # Mixed emotions: high magnitude but near-zero score for this user
        count_mixed = user_emotion_data.filter(emotion_score__gte=-0.2, emotion_score__lte=0.2, emotion_magnitude__gt=0.5).count()

        # Total chats and advices for this user
        total_chats = ChatLogs.objects.filter(user_id=pk).count()
        total_advices = AdviceData.objects.filter(user_id=pk).count()

        stats = {
            'avg_emotion_score': avg_emotion_score,
            'avg_emotion_magnitude': avg_emotion_magnitude,
            'count_positive': count_positive,
            'count_negative': count_negative,
            'count_neutral': count_neutral,
            'count_mixed': count_mixed,
            'total_chats': total_chats,
            'total_advices': total_advices
        }
        return Response(stats, status=status.HTTP_200_OK)

        

