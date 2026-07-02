from rest_framework import serializers
from app_accounts.models import User

class AdminRegisterSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    def create(self, validated_data):
        creator = self.context['request'].user
        return User.objects.create_admin(
            creator=creator,
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
