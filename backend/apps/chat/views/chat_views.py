from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from logging import getLogger

from apps.chat.serializers.chat_serializers import (
    ChatRequestSerializer,
    ChatMessageSerializer
)
from apps.chat.services.chat_services import (
    get_gpt_response,
    save_chat_message,
    get_chat_history
)

logger = getLogger(__name__)

class ChatView(APIView):
    """
    POST /chat
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = ChatRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user_message = serializer.validated_data['message']

            if not user_message:
                return Response({'detail': 'No message provided'}, status=422)

            # get message from GPT-4
            gpt_response = get_gpt_response(request.user, user_message)

            save_chat_message(request.user, user_message, gpt_response)

            return Response(
                {'gpt_response': gpt_response},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error in ChatView: {e}")
            return Response({'detail': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatHistoryView(APIView):
    """
    GET /chat/history
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            history_qs = get_chat_history(request.user)
            serializer = ChatMessageSerializer(history_qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in ChatHistoryView: {e}")
            return Response({'detail': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)