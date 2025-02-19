from django.urls import path

from users.views import UserRegisterAPIView, UserLoginAPIView

urlpatterns = [
    path('auth/register/', UserRegisterAPIView.as_view(), name='auth-register'),
    path('auth/login/', UserLoginAPIView.as_view(), name='auth-login'),
]