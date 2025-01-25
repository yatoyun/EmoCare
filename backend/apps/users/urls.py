from django.urls import path
from apps.users.views.users_views import (
    HealthView, 
    RegisterView, 
    LoginView, 
    LogoutView, 
    UserView
)

app_name = 'users'

urlpatterns = [
    path('health/', HealthView.as_view(), name='health'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
]
