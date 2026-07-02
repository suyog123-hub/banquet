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

#our Local apps
from app_accounts.serializers.login_serializer import LoginSerializer
from config.response import (
    success_response,
    error_response,
    validation_error_response,
    server_error_response,
    forbidden_response
)

class RefreshTokenAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        try:
            # Get refresh token from cookie
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return error_response(message="No refresh token found in cookies")

            try:
                # Validate refresh token and create new access token
                refresh = RefreshToken(refresh_token)
                new_access = refresh.access_token

                return success_response(
                    data={"access": str(new_access)},
                    message="Access token refreshed successfully"
                    )

            except (TokenError, InvalidToken):
                return forbidden_response(essage="Invalid or expired refresh token")

        except Exception as e:
            return server_error_response()