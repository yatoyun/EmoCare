from rest_framework import serializers
from apps.user_statistics.models import Statistics

class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ('id', 'emotion_score', 'emotion_magnitude', 'created_at')
        read_only_fields = ('id', 'created_at')
