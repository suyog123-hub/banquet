from django.shortcuts import render
from .serializer import BookingmodelSerializer
from .models import Bookingmodel
from rest_framework.views import  APIView
from config.permission import AdminGetOrPostAll
from config.response import *
from rest_framework import serializers
from config.pagination import Detailpage
from rest_framework.permissions import AllowAny
# Create your views here.

class Bookingview(APIView):
    pagination_class = Detailpage
    permission_classes =[AllowAny]
    def get(self,request):
        content = Bookingmodel.objects.all().order_by('id')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(content, request)
        serializer = BookingmodelSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        try:
            serializer = BookingmodelSerializer(data=request.data)
            if serializer.is_valid():
                print("suyog1")
                serializer.save()
                return success_response("Data post successfully",serializer.data)
            return validation_error_response(serializer.errors)
        except Exception:
            return server_error_response