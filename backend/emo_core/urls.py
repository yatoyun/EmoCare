from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .auth.views_auth import RegisterView, LoginView  # Import your auth views here
from . import views
from .line_bot.line_bot_api import callback


router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'emotionData', views.EmotionDataViewSet)
router.register(r'chatLogs', views.ChatLogsViewSet)
router.register(r'adviceData', views.AdviceDataViewSet)
router.register(r'userProfile', views.UserProfileViewSet)

# Create a custom route for the statistics view
statistics_list = views.StatisticsView.as_view({'get': 'list'})

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('statistics/', statistics_list, name='statistics-list'),
    path('callback/', callback, name='callback'),
]