from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.chat.serializers.chat_serializers import (
    ChatRequestSerializer,
    ChatMessageSerializer
)
from apps.chat.services.chat_services import (
    get_gpt_response,
    save_chat_message,
    get_chat_history
)

class ChatView(APIView):
    """
    POST /chat
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_message = serializer.validated_data['message']

        # get message from GPT-4
        try:
            gpt_response = get_gpt_response(request.user, user_message)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        chat_message = save_chat_message(request.user, user_message, gpt_response)

        return Response(
            {'gpt_response': gpt_response},
            status=status.HTTP_200_OK
        )


class ChatHistoryView(APIView):
    """
    GET /chat/history
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history_qs = get_chat_history(request.user)
        serializer = ChatMessageSerializer(history_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
