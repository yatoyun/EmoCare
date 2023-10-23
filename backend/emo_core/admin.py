from django.contrib import admin
from .models import UserModel, EmotionData, ChatLogs, AdviceData

admin.site.register(UserModel)
admin.site.register(EmotionData)
admin.site.register(ChatLogs)
admin.site.register(AdviceData)
