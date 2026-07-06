# accounts/serializers.py
from rest_framework import serializers
from app_accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "organization"]
