import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.users.models import User

@pytest.mark.django_db
class TestUserRegistration:
    def test_register_success(self):
        client = APIClient()
        url = reverse('users:register')
        data = {
            'name': 'testuser',
            'email': 'test@example.com',
            'password': 'secret'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 201
        assert User.objects.filter(email='test@example.com').exists()

    def test_register_email_already_exists(self):
        User.objects.create_user(name='exists', email='exists@example.com', password='secret')
        client = APIClient()
        url = reverse('users:register')
        data = {
            'name': 'testuser2',
            'email': 'exists@example.com',
            'password': 'secret'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400

@pytest.mark.django_db
class TestUserLogin:
    def test_login_success(self):
        User.objects.create_user(name='loginuser', email='login@example.com', password='secret')
        client = APIClient()
        url = reverse('users:login')
        data = {
            'email': 'login@example.com',
            'password': 'secret'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 200
        assert 'sessionid' in response.cookies

    def test_login_invalid(self):
        client = APIClient()
        url = reverse('users:login')
        data = {
            'password': 'secret'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 400

        data = {
            'email': 'notfound@example.com',
            'password': 'wrong'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == 401
