from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from app_accounts.models import User
from app_accounts.serializers.user_serializer import UserSerializer
from config.response import(
    success_response,
    not_found_response,
    unauthorized_response,
    error_response,
    validation_error_response,
    server_error_response
)


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if user.role == "admin":
                queryset = User.objects.all()
            elif user.role == "staff":
                queryset = User.objects.filter(organization=user.organization)
            else:
                queryset = User.objects.filter(id=user.id)

            serializer = UserSerializer(queryset, many=True)
            return success_response(data=serializer.data, message="User list retrieved successfully")
        except Exception as e:
            return server_error_response(str(e))


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, user):
        if user.role in ["admin", "superadmin"]:
            return User.objects.all()
        elif user.role == "staff":
            return User.objects.filter(organization=user.organization)
        else:
            return User.objects.filter(id=user.id)

    def get(self, request, ref_id):
        try:
            queryset = self.get_queryset(request.user)
            obj = get_object_or_404(queryset, ref_id=ref_id)
            serializer = UserSerializer(obj)
            return success_response(serializer.data, "User detail retrieved successfully")
        except Exception as e:
            return server_error_response(str(e))

    def put(self, request, ref_id):
        try:
            queryset = self.get_queryset(request.user)
            obj = get_object_or_404(queryset, ref_id=ref_id)

            serializer = UserSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_response(data=serializer.data, message="User updated successfully")
            return validation_error_response(errors=serializer.errors)
        except Exception as e:
            return server_error_response(str(e))

    def delete(self, request, ref_id):
        try:
            queryset = self.get_queryset(request.user)
            obj = get_object_or_404(queryset, ref_id=ref_id)
            obj.delete()
            return success_response(message="User deleted successfully", code=204)
        except Exception as e:
            return server_error_response(str(e))

