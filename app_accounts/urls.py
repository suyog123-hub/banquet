from django.urls import  path
from  app_accounts.views import RegisterUserAPIView, VerifyEmailView, LoginAPIView, RefreshTokenAPIView, LogoutAPIView, TestVIew
urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-otp'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]   
