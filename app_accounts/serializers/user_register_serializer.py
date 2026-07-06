from rest_framework import serializers
from app_accounts.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password", "role", "organization", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
         # If creating staff/admin, organization must be provided
        if data.get("role") in ["staff", "admin"] and not data.get("organization"):
            raise serializers.ValidationError({"organization": "Organization is required for staff/admin users"})
        
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        role = validated_data.get("role", "user")

        if role == "staff":
            # staff creation handled by manager
            user = User.objects.create_admin(
                creator=self.context["request"].user,
                **validated_data
            )
        elif role == "admin":
            # superuser creation (rare, usually via createsuperuser)
            user = User.objects.create_superuser(**validated_data)
        else:
            # normal user
            user = User.objects.create_user(**validated_data)

        return user

