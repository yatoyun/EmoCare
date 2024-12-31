from django.db import models
from django.utils import timezone
from django.conf import settings

class ChatMessage(models.Model):
    """
    Model to store chat history.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    user_message = models.TextField()
    gpt_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ChatMessage({self.user.email}): {self.user_message[:20]}..."
