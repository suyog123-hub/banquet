import uuid
import jwt
import datetime
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.views import APIView
from app_accounts.models import User
from config.response import (
    validation_error_response,
    created_response,
    success_response
)
from config.utils import generate_otp, store_otp, send_otp_email, verify_otp

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        user = request.user

        if not user.check_password(current_password):
            return validation_error_response({"current_password": "Incorrect old password"})

        user.set_password(new_password)
        user.save()

        return success_response({"message": "Password changed successfully"})


class RequestPasswordResetAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return validation_error_response({"email": "User not found"})

        otp = generate_otp()
        store_otp(user.id, otp, purpose="password_reset")
        send_otp_email(user.email, otp)
        return created_response({"message": "OTP sent to email"})


class VerifyPasswordResetOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return validation_error_response({"email": "User not found"})

        valid, error = verify_otp(user.id, otp, "password_reset")
        if not valid:
            return validation_error_response({"otp": error})

        # Generate JWT reset token
        payload = {
            "user_id": user.id,
            "purpose": "password_reset",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            "iat": datetime.datetime.utcnow(),
        }
        reset_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return created_response(data={
            "message": "OTP verified. Use this token to reset password.",
            "reset_token": reset_token
        })




class ResetPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        reset_token = request.data.get("reset_token")

        if not email or not new_password or not reset_token:
            return validation_error_response({"error": "Email, new password, and reset token are required"})

        try:
            payload = jwt.decode(reset_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return validation_error_response({"error": "Reset token expired"})
        except jwt.InvalidTokenError:
            return validation_error_response({"error": "Invalid reset token"})

        if payload.get("purpose") != "password_reset":
            return validation_error_response({"error": "Invalid token purpose"})

        try:
            user = User.objects.get(id=payload["user_id"], email=email)
        except User.DoesNotExist:
            return validation_error_response({"email": "User not found"})

        # if valid Reset password
        user.set_password(new_password)
        user.save()

        return success_response({"message": "Password reset successful"})


