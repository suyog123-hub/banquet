# serializers.py
from rest_framework import serializers
from .models import Bookingmodel
import re
from datetime import datetime
from django.utils import timezone

class BookingmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookingmodel
        fields = '__all__'
        extra_kwargs = {
            "user": {"read_only":True },
        }
    
    def validate_name(self, value):
        """Validate name: at least 2 characters, letters only."""
        if len(value) < 2 or len(value) > 60:
            raise serializers.ValidationError("Name must be at between  2 and 60 characters long.")
        return value.strip()
    
    def validate_contact(self, value):
        phone = str(value)
        # Nepal mobile: 10 digits starting with 9
        if not re.match(r'^9\d{9}$', phone):
            raise serializers.ValidationError(
                "Invalid phone number. Must be a 10-digit Nepal mobile number starting with 9."
            )
        return value
    
    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Invalid email address format.")
        return value.lower()
    
    def validate_booking_date(self, value):
        today = timezone.now().date()
        
        if value < today:
            raise serializers.ValidationError("Booking date cannot be in the past.")
        
        return value
    
    def validate_number_of_guest(self, value):
        if value < 1 or value > 1000 :
            raise serializers.ValidationError("Number of guests must be at minimum 1 and maximum 1000.")
        return value
    
    def validate_details(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError("Details must be at least 5 characters long.")
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        validated_data['created_by'] = self.context["request"].user
        return super().create(validated_data)