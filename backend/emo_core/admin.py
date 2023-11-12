from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import UserModel, UserProfile, EmotionData, ChatLogs, AdviceData

admin.site.register(UserModel)
admin.site.register(EmotionData)
admin.site.register(ChatLogs)
admin.site.register(AdviceData)
admin.site.register(UserProfile)
admin.site.register(Session)