from django.urls import path
from .auth.views_auth import RegisterView, LoginView  # Import your auth views here

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # ... other url patterns
]