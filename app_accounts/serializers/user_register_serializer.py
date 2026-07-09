import re
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from app_accounts.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password", "role", "organization", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        
    def validate_first_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("First name cannot contain numbers")
        return value

    def validate_last_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Last name cannot contain numbers")
        return value

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        elif not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number")
        elif not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        return value
    

    def validate_first_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("First name cannot contain numbers")
        return value.capitalize()

    def validate_last_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Last name cannot contain numbers")
        return value.capitalize()
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        return value


    def validate_email_field(value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        
         # If creating staff/admin, organization must be provided
        if data.get("role") in ["staff", "admin"] and not data.get("organization"):
            raise serializers.ValidationError("Organization is required for staff/admin users")
        
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        role = validated_data.get("role", "user")

        if role == "staff":
            # staff creation handled by manager
            user = User.objects.create_staff(
                creator=self.context["request"].user,
                **validated_data,
            )
        elif role == "admin":
            # superuser creation (rare, usually via createsuperuser)
            user = User.objects.create_admin(**validated_data)
        else:
            # normal user
            user = User.objects.create_user(**validated_data)

        return user

