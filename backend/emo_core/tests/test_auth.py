from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AuthTests(APITestCase):

    def test_register_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('register')  # Replace with the actual URL name for your register view
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_login_user(self):
        """
        Ensure we can login a user.
        """
        # First, create a user that can be logged in
        self.test_register_user()

        url = reverse('login')  # Replace with the actual URL name for your login view
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Logged in successfully')

# Update the URL names 'register' and 'login' based on what you have defined in your urls.py
