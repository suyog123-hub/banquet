# Standard library
from django.utils.timezone import now

# Third-party
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError, InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from django.core.cache import cache

#our Local apps
from app_accounts.serializers.login_serializer import LoginSerializer
from config.response import (
    success_response,
    error_response,
    validation_error_response,
    forbidden_response,
    server_error_response,
    not_found_response
)
from config.logging import *
from app_accounts.throttles import LoginViewThrottle
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginViewThrottle]
    @staticmethod
    def get_tokens_for_user(user):
        if not user.is_active:
            raise AuthenticationFailed("User is not active")
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']

                # Cache keys
                attempts_key = f"login_attempts_{username}"
                lockout_key = f"lockout_{username}"

                # Check lockout
                if cache.get(lockout_key):
                    return forbidden_response(
                        message={"detail": "Too many failed attempts. Try again after 15 minutes."}
                    )

                user = authenticate(username=username, password=password)
                if user is not None:
                    if not user.is_active:
                        return forbidden_response(message={"detail": "Account is locked. Contact admin."})
                    
                    tokens = self.get_tokens_for_user(user)

                    # Reset attempts on success
                    cache.delete(attempts_key)

                    response = success_response(
                        message="Login Success",
                        data={"access": tokens['access']}
                    )
                    response.set_cookie(
                        key='refresh_token',
                        value=tokens['refresh'],
                        httponly=True,
                        secure=True,
                        samesite='Lax',
                        max_age=60*60*24*7
                    )
                    return response

                # Invalid credentials → increment attempts
                attempts = cache.get(attempts_key, 0) + 1
                cache.set(attempts_key, attempts, timeout=60*60)

                if attempts >= 3:
                    cache.set(lockout_key, True, timeout=60*15)  # 15 minutes
                    cache.delete(attempts_key)
                    return forbidden_response(
                        message={"detail": "Too many failed attempts. Your account is temporarily locked for 15 minutes."}
                    )

                return error_response(message="Invalid Credentials")

            return validation_error_response(message="Invalid request data")

        except Exception as e:
            logger.error(str(e), exc_info=True)
            return server_error_response()


    