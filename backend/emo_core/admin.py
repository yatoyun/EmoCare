from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import UserModel, UserProfile, EmotionData, ChatLogs, AdviceData, TempRegisterToken

admin.site.register(UserModel)
admin.site.register(EmotionData)
admin.site.register(ChatLogs)
admin.site.register(AdviceData)
admin.site.register(UserProfile)
admin.site.register(Session)
admin.site.register(TempRegisterToken)