from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UserModel(AbstractUser):
    line_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class TempRegisterToken(models.Model):
    line_user_id = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    expiration = models.DateTimeField()

    def __str__(self):
        return self.line_user_id
    
    def is_expired(self):
        return timezone.now() >= self.expiration

class TemporaryCode(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expiration = models.DateTimeField()

    def is_expired(self):
        return timezone.now() >= self.expiration

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