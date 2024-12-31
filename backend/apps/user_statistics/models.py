from django.db import models
from django.utils import timezone
from django.conf import settings

class Statistics(models.Model):
    """
    Model to store user_statistics.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_statistics'
    )
    emotion_score = models.FloatField()
    emotion_magnitude = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Statistics({self.user.email}): {self.emotion_score}..."
