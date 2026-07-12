from django.urls import  path
from  app_accounts.views import (
    RegisterUserAPIView, VerifyEmailView, 
    StaffRegisterAPIView,ResendOTPAPIView,
    LoginAPIView, RefreshTokenAPIView, 
    LogoutAPIView, UserDeactivate,
    RequestPasswordResetAPIView,
    VerifyPasswordResetOTPAPIView,
    ResetPasswordAPIView,
    ChangePasswordAPIView
    )
urlpatterns = [
    # for register, login and logout
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('register/staff/', StaffRegisterAPIView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPAPIView.as_view(), name='resed-otp'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh-token/', RefreshTokenAPIView.as_view(), name='refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('deactivate/', UserDeactivate.as_view(), name='deactivate'),
    
    # for password change or reset
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('request-password-reset/', RequestPasswordResetAPIView.as_view(), name='request-password-reset'),
    path('verify-password-reset/', VerifyPasswordResetOTPAPIView.as_view(), name='verify-password-reset'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]   
