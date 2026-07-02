from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError({"error": "Invalid credentials"})
            if not user.is_active:
                raise serializers.ValidationError({"error": "Account not verified"})
            data["user"] = user
        else:
            raise serializers.ValidationError({"error": "Must include username and password"})
        return data
