from rest_framework.views import APIView
from app_accounts.serializers.user_register_serializer import UserRegistrationSerializer
from config.utils import generate_otp, store_otp, send_otp_email
from config.response import (
    created_response,
    validation_error_response,
    server_error_response
)
class RegisterUserAPIView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data = request.data)
            if serializer.is_valid():
                user = serializer.save()
                otp = generate_otp()
                store_otp(user.id, otp, purpose="email_verification")
                send_otp_email(user.email, otp)
                return created_response({"data":serializer.data, "user_id":user.id})
            return validation_error_response(serializer.errors)
        except Exception as e:
            return server_error_response(str(e))
    