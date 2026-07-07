from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from app_accounts.serializers.user_register_serializer import UserRegistrationSerializer
from config.utils import generate_otp, store_otp, send_otp_email
from django.core.mail import send_mail
from app_accounts.throttles import OTPResendThrottle
from app_accounts.models import User
from threading import Thread
from django.conf import settings
from config.response import (
    created_response,
    error_response,
    validation_error_response,
    server_error_response,
    not_found_response,
    forbidden_response
)

class StaffRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if not request.user.is_superuser:
                return forbidden_response("Only superusers can create staff", 403)
            data = request.data.copy()
            # making a copy of request.data and enforcing role as staff for organization validation
            data['role'] = "staff"
            serializer = UserRegistrationSerializer(data=data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data.pop("confirm_password")
                user = User.objects.create_staff(creator=request.user, **serializer.validated_data)
                # for sending emails
                subject = "Thankyou Mail !!!"
                message = f"""
                Dear {user.first_name},

                This is to confirm that your account has been created successfully.

                Best regards,
                Sajha Info Tech
                """
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                
                thread = Thread(
                    target=send_mail,
                    args=(subject, message, from_email, recipient_list, True),
                    daemon=True
                )
                thread.start()

                return created_response(data={"user_id": user.id, "data": serializer.data}, message="Staff registered successfully")
            return validation_error_response(serializer.errors)
        except Exception as e:
            return server_error_response(str(e))



class RegisterUserAPIView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data = request.data)
            if serializer.is_valid():
                user = serializer.save()
                otp = generate_otp()
                store_otp(user.id, otp, purpose="email_verification")
                # for sending email in background using daemon
                # send_otp_email(user.email, otp)
                thread = Thread(
                    target=send_otp_email,
                    args=(user.email, otp),
                    daemon=True
                )
                thread.start()
                return created_response({"data":serializer.data, "user_id":user.id})
            return validation_error_response(serializer.errors)
        except Exception as e:
            return server_error_response(str(e))
        
        
class ResendOTPAPIView(APIView):
    throttle_classes = [OTPResendThrottle]

    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return validation_error_response({"user_id": "User ID is required"})

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return not_found_response(message="User not found", code=404)

        otp = generate_otp()
        store_otp(user.id, otp, purpose="email_verification")
        thread = Thread(
                    target=send_otp_email,
                    args=(user.email, otp),
                    daemon=True
                )
        thread.start()

        return created_response({"message": "New OTP sent successfully"})
    