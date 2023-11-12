from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .auth.views_auth import RegisterView, CustomTokenObtainPairView, CustomRefreshTokenView, LogoutView  # Import your auth views here
from . import views
from .line_bot.line_bot_api import callback


router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'emotionData', views.EmotionDataViewSet)
router.register(r'chatLogs', views.ChatLogsViewSet)
router.register(r'adviceData', views.AdviceDataViewSet)
router.register(r'userProfile', views.UserProfileViewSet)
router.register(r'statistics', views.StatisticsView, basename='statistics')


# Create a custom route for the statistics view
statistics_list = views.StatisticsView.as_view({'get': 'list'})

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('callback/', callback, name='callback'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]