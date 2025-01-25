from django.contrib.auth import authenticate
from typing import Optional
import logging
from apps.users.models import User

logger = logging.getLogger(__name__)

def register_user(name: str, email: str, password: str) -> User:
    if not name or not email or not password:
        raise ValueError("All fields (name, email, password) are required")
        
    if User.objects.filter(email=email).exists():
        raise ValueError("This email is already registered")
        
    if User.objects.filter(name=name).exists():
        raise ValueError("This username is already taken")

    user = User.objects.create_user(
        name=name,
        email=email,
        password=password
    )
    return user

def login_user(name: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> User:
    if not password:
        raise ValueError("Password is required")
    
    if not (name or email):
        raise ValueError("Authentication requires either username or email")
    
    if name and email:
        raise ValueError("Please provide either username or email, not both")

    if name:
        try:
            user_obj = User.objects.get(name=name)
            if not user_obj.check_password(password):
                raise ValueError("Invalid password")
            return user_obj
        except User.DoesNotExist:
            raise ValueError("User not found with this username")

    if email:
        user = authenticate(username=email, password=password)
        if not user:
            raise ValueError("Invalid email or password")
        return user
