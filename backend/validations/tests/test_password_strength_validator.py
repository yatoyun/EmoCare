import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from validations.password_strength_validator import PasswordStrengthValidator

User = get_user_model()

class TestPasswordStrengthValidator:
    """
    Test cases for the enhanced password strength validator
    """
    
    def test_weak_passwords_rejected(self):
        """Test that weak passwords are rejected with detailed feedback"""
        validator = PasswordStrengthValidator()
        
        weak_passwords = [
            "password",
            "123456",
            "qwerty", 
            "abc123",
            "password123"
        ]
        
        for weak_password in weak_passwords:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(weak_password)
            
            error = exc_info.value
            assert error.code == 'password_too_weak'
            # Error message should be in Japanese
            assert any(char in error.message for char in ['パスワード', '弱い', '推測'])
    
    def test_strong_passwords_accepted(self):
        """Test that strong passwords are accepted"""
        validator = PasswordStrengthValidator()
        
        strong_passwords = [
            "MyVeryStr0ngP@ssw0rd!",
            "Th1s1sAn0therStr0ngP@ssw0rd",
            "Un1que$ecureP@ssw0rd2024",
            "C0mpl3xP@ssw0rd!W1thSymb0ls"
        ]
        
        for strong_password in strong_passwords:
            # Should not raise any exception
            validator.validate(strong_password)
    
    def test_user_context_awareness(self):
        """Test that validator uses user context to reject personal information"""
        validator = PasswordStrengthValidator()
        
        # Create a test user
        user = User(email="test@example.com", name="testuser")
        
        # Passwords containing user information should be rejected
        user_related_passwords = [
            "testuser123",
            "test@example.com",
            "testexample",
        ]
        
        for password in user_related_passwords:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(password, user=user)
            
            error = exc_info.value
            assert error.code == 'password_too_weak'
    
    def test_configurable_score_threshold(self):
        """Test that score threshold can be configured"""
        # More lenient validator (score >= 1)
        lenient_validator = PasswordStrengthValidator(min_score=1)
        
        # Stricter validator (score >= 3)
        strict_validator = PasswordStrengthValidator(min_score=3)
        
        medium_strength_password = "password123A"
        
        # Should pass lenient validation
        lenient_validator.validate(medium_strength_password)
        
        # Should fail strict validation
        with pytest.raises(ValidationError):
            strict_validator.validate(medium_strength_password)
    
    def test_detailed_error_messages(self):
        """Test that detailed error messages are provided"""
        validator = PasswordStrengthValidator()
        
        test_cases = [
            ("password", "一般的"),  # Common password
            ("abcdef", "連続"),       # Sequential
            ("aaaaaa", "繰り返し"),   # Repeated
            ("123456", "推測"),      # Predictable
        ]
        
        for password, expected_keyword in test_cases:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(password)
            
            error = exc_info.value
            # Check that the error message contains relevant feedback
            assert any(keyword in error.message for keyword in [expected_keyword, "パスワード"])
    
    def test_help_text(self):
        """Test that help text is provided in Japanese"""
        validator = PasswordStrengthValidator()
        help_text = validator.get_help_text()
        
        assert "パスワード" in help_text
        assert "強力" in help_text
    
    def test_no_user_context(self):
        """Test validator works when no user context is provided"""
        validator = PasswordStrengthValidator()
        
        # Should work without user
        validator.validate("MyStr0ngP@ssw0rd!")
        
        # Should still reject weak passwords
        with pytest.raises(ValidationError):
            validator.validate("weak")
    
    def test_score_levels_feedback(self):
        """Test that different score levels provide appropriate feedback"""
        validator = PasswordStrengthValidator(min_score=0)  # Allow all to test messages
        
        score_test_cases = [
            ("a", "非常に弱い"),      # Score 0
            ("password", "弱い"),      # Score 1  
        ]
        
        for password, expected_strength in score_test_cases:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(password)
            
            error = exc_info.value
            assert expected_strength in error.message
    
    def test_user_with_missing_attributes(self):
        """Test validator handles user objects with missing attributes gracefully"""
        validator = PasswordStrengthValidator()
        
        # Mock user with only some attributes
        class PartialUser:
            def __init__(self, email=None, name=None):
                if email:
                    self.email = email
                if name:
                    self.name = name
        
        # Should not crash with partial user info
        user_no_email = PartialUser(name="testuser")
        validator.validate("MyStr0ngP@ssw0rd!", user_no_email)
        
        user_no_name = PartialUser(email="test@example.com")
        validator.validate("MyStr0ngP@ssw0rd!", user_no_name)
        
        user_empty = PartialUser()
        validator.validate("MyStr0ngP@ssw0rd!", user_empty)