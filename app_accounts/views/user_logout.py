# Standard library
from django.utils.timezone import now

# Third-party
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login

# local apps
from config.response import (
    success_response,
    error_response,
    validation_error_response,
    server_error_response,
    not_found_response
)
from config.logging import *

class LogoutAPIView(APIView):
    authentication_classes = JWTAuthentication
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return error_response(message="No refresh token found in cookies")

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (TokenError, InvalidToken):
                return error_response(message="Invalid or expired refresh token")

            response = success_response(message="Logged out successfully")

            response.delete_cookie(
                "refresh_token",
                samesite='Lax'
            )
            return response
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return server_error_response()
