from rest_framework import serializers

from apps.chat.models import ChatMessage

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField()

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value

class ChatMessageSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(source='created_at', format='%Y-%m-%dT%H:%M:%S%z', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ('timestamp', 'user_message', 'gpt_response')
