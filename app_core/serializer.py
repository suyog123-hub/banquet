# serializers.py
from rest_framework import serializers
from .models import WeddingPalace
import re


class WeddingPalaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingPalace
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def validate_contact_number(self, value):
        phone = re.sub(r'[\s\-\(\)]', '', value)
        if not re.match(r'^9\d{9}$', phone):
            raise serializers.ValidationError(
                "Invalid phone number. Must be a 10-digit Nepal mobile number starting with 9."
            )
        return phone
    
    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Only Gmail addresses are allowed.')
        return value

    def validate_base_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Base price must be greater than 0.")
        return value


    def validate_description(self , value):
        if len(value)< 5 :
            raise serializers.ValidationError("please write more description")
        return value
    
    