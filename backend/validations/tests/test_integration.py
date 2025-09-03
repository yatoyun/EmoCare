import pytest
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.users.models import User

@pytest.mark.django_db
class TestPasswordValidationIntegration:
    """
    Integration tests to verify password validation works with user registration
    """
    
    def test_registration_with_weak_password_fails(self):
        """Test that user registration fails with weak password"""
        client = APIClient()
        url = reverse('users:register')
        
        # Test with various weak passwords
        weak_password_data = [
            {
                'name': 'testuser1',
                'email': 'test1@example.com', 
                'password': 'password'  # Common password
            },
            {
                'name': 'testuser2',
                'email': 'test2@example.com',
                'password': '123456'  # Sequential numbers
            },
            {
                'name': 'testuser3', 
                'email': 'test3@example.com',
                'password': 'testuser3'  # Contains username
            }
        ]
        
        for data in weak_password_data:
            response = client.post(url, data, format='json')
            
            # Should fail with 400 status
            assert response.status_code == 400
            
            # Should contain validation error details
            assert 'errors' in response.data
            assert 'password' in response.data['errors']
            
            # Error message should be in Japanese
            password_errors = response.data['errors']['password']
            assert any('パスワード' in str(error) for error in password_errors)
            
            # User should not be created
            assert not User.objects.filter(email=data['email']).exists()
    
    def test_registration_with_strong_password_succeeds(self):
        """Test that user registration succeeds with strong password"""
        client = APIClient()
        url = reverse('users:register')
        
        data = {
            'name': 'testuser',
            'email': 'test@example.com',
            'password': 'MyVeryStr0ngP@ssw0rd!'  # Strong password
        }
        
        response = client.post(url, data, format='json')
        
        # Should succeed with 201 status
        assert response.status_code == 201
        
        # User should be created
        assert User.objects.filter(email=data['email']).exists()
        
        # User should be logged in (session created)
        assert 'sessionid' in response.cookies
    
    def test_user_update_password_validation(self):
        """Test that password validation works when updating user password"""
        # Create a user first
        user = User.objects.create_user(
            name='updateuser',
            email='update@example.com',
            password='TempStr0ngP@ss!'
        )
        
        client = APIClient()
        client.force_login(user)
        url = reverse('users:user')
        
        # Try to update with weak password
        weak_data = {
            'email': 'update@example.com',
            'password': 'weak'  # Weak password
        }
        
        response = client.patch(url, weak_data, format='json')
        
        # Should fail with validation error
        assert response.status_code == 400
        
        # Should contain password validation error
        assert 'password' in response.data
        
        # Try to update with strong password
        strong_data = {
            'email': 'update@example.com', 
            'password': 'NewStr0ngP@ssw0rd!'
        }
        
        response = client.patch(url, strong_data, format='json')
        
        # Should succeed
        assert response.status_code == 200
        
        # Verify password was updated
        user.refresh_from_db()
        assert user.check_password('NewStr0ngP@ssw0rd!')
    
    def test_password_validation_with_user_context(self):
        """Test that user context is considered during registration"""
        client = APIClient()
        url = reverse('users:register')
        
        # Password containing email username should be rejected
        data = {
            'name': 'contexttest',
            'email': 'contexttest@example.com',
            'password': 'contexttest123'  # Contains username
        }
        
        response = client.post(url, data, format='json')
        
        # Should fail due to user context validation
        assert response.status_code == 400
        assert 'errors' in response.data
        assert 'password' in response.data['errors']
        
        # User should not be created
        assert not User.objects.filter(email=data['email']).exists()