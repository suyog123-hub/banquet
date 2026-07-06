from .models import BlogCategory ,Content
from rest_framework import serializers
from datetime import timezone
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields ="__all__"
        read_only_fields = []

    def validate_title(self,value):
        if len(value) <2 :
            return serializers.ValidationError("length of title should be  more that 2")
        


class Contentserializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields ="__all__"

    def validate_heading(self,value):
        if len(value) <2 :
            return serializers.ValidationError("length of heading should be  more that 2")
        
    
    def validate_content(self, value):
        if len(value)< 10 :
            raise serializers.ValidationError("please enter  the more content")

        

    
        