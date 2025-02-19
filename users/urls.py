from django.urls import path

from users.views import UserRegisterAPIView

urlpatterns = [
    path('auth/register/', UserRegisterAPIView.as_view(), name='auth-register'),
]