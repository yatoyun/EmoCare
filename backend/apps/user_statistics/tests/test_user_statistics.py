import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.users.models import User
from apps.user_statistics.models import Statistics

@pytest.mark.django_db
class TestStatisticsView:
    def test_get_statistics_authenticated(self):
        # create test user
        user = User.objects.create_user(email='test@example.com', name='test', password='secret')

        # create dummy statistics data
        Statistics.objects.create(user=user, emotion_score=0.5, emotion_magnitude=1.2)
        Statistics.objects.create(user=user, emotion_score=0.8, emotion_magnitude=2.0)

        client = APIClient()
        # assume login (session authentication)
        client.login(username='test@example.com', password='secret')

        url = reverse('user_statistics:user_statistics')
        response = client.get(url, format='json')
        assert response.status_code == 200
        assert len(response.data) == 10

    def test_get_statistics_forbidden(self):
        client = APIClient()
        url = reverse('user_statistics:user_statistics')
        response = client.get(url)
        assert response.status_code == 403
