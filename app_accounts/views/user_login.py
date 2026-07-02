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
from django.contrib.auth import authenticate, login

#our Local apps
from app_accounts.serializers.login_serializer import LoginSerializer
from config.response import (
    success_response,
    error_response,
    validation_error_response,
    server_error_response,
    not_found_response
)


class TestVIew(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response('This is protected view')
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
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
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    tokens = self.get_tokens_for_user(user)
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
                return not_found_response(message="No such user exists")
            return error_response(message="Invalid Credentials")
        except Exception as e:
            return server_error_response(message="Internal server error")

    