from .models import contact
from rest_framework import serializers
import re

class Contactserializer(serializers.ModelSerializer):
    class Meta:
        model = contact
        fields = "__all__"
    
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name should be greater than 2 characters.")
        return value
    
    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Only Gmail addresses are allowed.')
        return value
    
    def validate_phone(self, value):
        pattern = r'^9\d{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid Nepal mobile number. Must be 10 digits starting with 9.")
        return value