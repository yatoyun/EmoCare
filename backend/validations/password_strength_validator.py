from django.core.exceptions import ValidationError
from zxcvbn import zxcvbn

class PasswordStrengthValidator:
    def validate(self, password, user=None):
        results = zxcvbn(password)
        if results['score'] < 2:
            raise ValidationError(
                'Password too weak. Try using a stronger password.',
                code='password_too_weak',
            )
