from rest_framework import serializers
from .models import UserModel, EmotionData, ChatLogs, AdviceData

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password', 'email', 'line_user_id')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('line_user_id',)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
            )
        return user

class EmotionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionData
        fields = ('id', 'user', 'emotion_score', 'emotion_magnitude', 'created_at', 'updated_at')
        read_only_fields = ('user',)  # These fields should not be editable

class ChatLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLogs
        fields = ('id', 'user', 'message', 'created_at')
        read_only_fields = ('user',)  # This field should not be editable

class AdviceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviceData
        fields = ('id', 'user', 'advice', 'effectiveness', 'created_at', 'updated_at')
        read_only_fields = ('user',)  # These fields should not be editable
