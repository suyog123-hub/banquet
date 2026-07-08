from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_accounts.models import User
from django.core.cache import cache
from config.response import (
    success_response,
    error_response,
    validation_error_response,
    server_error_response,
    not_found_response
)
from config.logging import *

def verify_otp(user_id, otp, expected_purpose):
    try:
        cache_key = f"otp:{user_id}"
        stored_data = cache.get(cache_key)

        if stored_data is None:
            return False, "OTP expired or not found"

        if stored_data.get("otp") != otp:
            return False, "Invalid OTP"

        if stored_data.get("purpose") != expected_purpose:
            return False, "OTP purpose mismatch"

        # OTP is valid
        cache.delete(cache_key)
        return True, None
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return server_error_response()


class VerifyEmailView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            otp = request.data.get("otp")

            if not user_id or not otp:
                return error_response(message="User ID and OTP are required")

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return not_found_response(message="User not found", code=404)

            valid, error = verify_otp(user.id, otp, "email_verification")
            if not valid:
                return error_response(message=error)

            user.is_active = True
            user.save()
            return success_response(message="Email verified successfully")
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return server_error_response()


