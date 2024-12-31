from django.urls import path
from apps.users.views.users_views import RegisterView, LoginView, UserDetailView, UpdateUserView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('user/', UpdateUserView.as_view(), name='user_update'),
]
