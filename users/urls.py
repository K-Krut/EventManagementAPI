from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import UserRegisterAPIView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path('auth/register/', UserRegisterAPIView.as_view(), name='auth-register'),
    path('auth/login/', UserLoginAPIView.as_view(), name='auth-login'),
    path('auth/logout/', UserLogoutAPIView.as_view(), name='auth-logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]