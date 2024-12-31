import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.users.models import User
from apps.chat.models import ChatMessage

@pytest.mark.django_db
class TestChat:
    def test_chat_post(self):
        """
        /chat POST sends a message, GPT response is returned, and saved in the DB.
        """
        user = User.objects.create_user(email='test@example.com', name='test', password='secret')
        client = APIClient()
        client.login(username='test@example.com', password='secret')  # SessionAuthenticationの場合

        url = reverse('chat:chat')  # apps/chat/urls.py の name='chat' を想定
        data = {'message': 'Hello GPT!'}
        response = client.post(url, data, format='json')

        assert response.status_code == 200
        assert 'gpt_response' in response.data
        assert ChatMessage.objects.count() == 1

    def test_chat_forbidden(self):
        """
        /chat POST without authentication returns 403.
        """
        client = APIClient()
        url = reverse('chat:chat')
        data = {'message': 'No user'}
        response = client.post(url, data, format='json')

        assert response.status_code == 403

@pytest.mark.django_db
class TestChatHistory:
    def test_chat_history_get(self):
        user = User.objects.create_user(email='test2@example.com', name='test2', password='secret')
        ChatMessage.objects.create(user=user, user_message='Hello', gpt_response='Hi',)
        ChatMessage.objects.create(user=user, user_message='How are you?', gpt_response='I am fine',)

        client = APIClient()
        client.login(username='test2@example.com', password='secret')

        url = reverse('chat:history')
        response = client.get(url, format='json')

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_chat_history_forbidden(self):
        client = APIClient()
        url = reverse('chat:history')
        response = client.get(url)
        assert response.status_code == 403
