from rest_framework import viewsets, views, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import UserModel, UserProfile, EmotionData, ChatLogs, AdviceData, TemporaryCode
from django.db.models import Avg, Max, Min, Count, StdDev, Variance, Sum, Q
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .serializers import UserModelSerializer, UserProfileSerializer, EmotionDataSerializer, ChatLogsSerializer, AdviceDataSerializer
from scipy import stats



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
            try:
                user.delete()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"status": "User deleted"}, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
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

@permission_classes([IsAuthenticated])
class ResetPassword(views.APIView):
    def post(self, request):
        temp_code = request.data.get('oneTimePassword')
        new_password = request.data.get('password')  # 新しいパスワード

        user = request.user  # 現在の認証ユーザーを取得
        try:
            temporary_code = TemporaryCode.objects.get(user=user, code=temp_code)

            if not temporary_code.is_expired():
                # 新しいパスワードでユーザーのパスワードを更新
                try:
                    validate_password(new_password, user)
                    user.set_password(new_password)
                    user.save()
                except ValidationError as e:
                    return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
                
                # 一時使用コードの削除
                temporary_code.delete()

                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired temporary code."}, status=status.HTTP_400_BAD_REQUEST)

        except TemporaryCode.DoesNotExist:
            return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)



class EmotionDataViewSet(viewsets.ModelViewSet):
    queryset = EmotionData.objects.all()
    serializer_class = EmotionDataSerializer

class ChatLogsViewSet(viewsets.ModelViewSet):
    queryset = ChatLogs.objects.all()
    serializer_class = ChatLogsSerializer

class AdviceDataViewSet(viewsets.ModelViewSet):
    queryset = AdviceData.objects.all()
    serializer_class = AdviceDataSerializer

@permission_classes([IsAuthenticated])
class StatisticsView(viewsets.ViewSet):
    def list(self, request):
        ####### EmotionData statistics ########
        if not request.user or not request.user.is_authenticated:
            return Response({'error': 'need authorization'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = request.user
            emotion_data = EmotionData.objects.filter(user=user)
        
            emotion_scores = list(emotion_data.values_list('emotion_score', flat=True))
            emotion_magnitudes = list(emotion_data.values_list('emotion_magnitude', flat=True))
            
            

            ####### Time series analysis for trends #######
            daily_emotion_stats = emotion_data.annotate(date=TruncDay('created_at')).values('date').annotate(
                avg_score=Avg('emotion_score'),
                count=Count('id')
            ).order_by('date')
            
            weekly_emotion_stats = emotion_data.annotate(week=TruncWeek('created_at')).values('week').annotate(
                avg_score=Avg('emotion_score'),
                count=Count('id')
            ).order_by('week')

            ####### ChatLogs statistics - total number of messages and total message length #######
            # per date
            daily_chat_stats = ChatLogs.objects.annotate(date=TruncDay('created_at')).values('date').annotate(
                total_messages=Count('id'),
            ).order_by('date')
            # per week
            weekly_chat_stats = ChatLogs.objects.annotate(week=TruncWeek('created_at')).values('week').annotate(
                total_messages=Count('id'),
            ).order_by('week')
            
            ####### sentiment classification 
            # Daily
            daily_sentiment_classification = emotion_data.annotate(
                date=TruncDay('created_at')
            ).values('date').annotate(
                positive=Count('id', filter=Q(emotion_score__gt=0.25)),
                negative=Count('id', filter=Q(emotion_score__lt=-0.25)),
                neutral=Count('id', filter=Q(emotion_score__gte=-0.15, emotion_score__lte=0.15)),
                mixed=Count('id', filter=Q(emotion_score__gt=-0.15, emotion_score__lt=0.15, emotion_magnitude__gt=0.5))
            ).order_by('date')

            # Weekly
            weekly_sentiment_classification = emotion_data.annotate(
                week=TruncWeek('created_at')
            ).values('week').annotate(
                positive=Count('id', filter=Q(emotion_score__gt=0.25)),
                negative=Count('id', filter=Q(emotion_score__lt=-0.25)),
                neutral=Count('id', filter=Q(emotion_score__gte=-0.15, emotion_score__lte=0.15)),
                mixed=Count('id', filter=Q(emotion_score__gt=-0.15, emotion_score__lt=0.15, emotion_magnitude__gt=0.5))
            ).order_by('week')


            ####### Scatter plot data for emotion score vs. magnitude 
            scatter_data = list(zip(emotion_scores, emotion_magnitudes))

            # Correlation and descriptive statistics
            correlation_score_magnitude = stats.pearsonr(emotion_scores, emotion_magnitudes)[0]
            skewness = stats.skew(emotion_scores)
            kurtosis = stats.kurtosis(emotion_scores)

            # Descriptive context for skewness and kurtosis
            descriptive_skewness = "positive" if skewness > 0 else "negative"
            descriptive_kurtosis = "less reliable" if kurtosis > 3 else "reliable"

            # Prepare the response data
            stats_response = {
                'daily_emotion_stats': list(daily_emotion_stats),
                'weekly_emotion_stats': list(weekly_emotion_stats),
                'daily_chat_stats': list(daily_chat_stats),
                'weekly_chat_stats': list(weekly_chat_stats),
                'daily_sentiment_classification': list(daily_sentiment_classification),
                'weekly_sentiment_classification': list(weekly_sentiment_classification),
                'scatter_data': scatter_data,
                'correlation_score_magnitude': correlation_score_magnitude,
                'skewness': {'value': skewness, 'description': descriptive_skewness},
                'kurtosis': {'value': kurtosis, 'description': descriptive_kurtosis},
            }

            return Response(stats_response)
        
        except EmotionData.DoesNotExist:
            return Response({'error': 'cannot find data'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
