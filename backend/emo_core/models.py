from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    line_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
class TempRegister(models.Model):
    line_user_id = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.line_user_id

class EmotionData(models.Model):
    user = models.ForeignKey(UserModel, related_name='emotion_data', on_delete=models.CASCADE)
    emotion_score = models.FloatField()
    emotion_magnitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
class ChatLogs(models.Model):
    user = models.ForeignKey(UserModel, related_name='chat_logs', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class AdviceData(models.Model):
    user = models.ForeignKey(UserModel, related_name='advice_data', on_delete=models.CASCADE)
    advice = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)