from django.urls import path
from apps.chat.views.chat_views import ChatView, ChatHistoryView

app_name = 'chat'

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),            # POST /chat
    path('history/', ChatHistoryView.as_view(), name='history'),  # GET /chat/history
]
