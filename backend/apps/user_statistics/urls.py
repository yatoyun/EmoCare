from django.urls import path
from apps.user_statistics.views.user_statistics_views import StatisticsView

app_name = 'user_statistics'

urlpatterns = [
    path('', StatisticsView.as_view(), name='user_statistics'),
]
