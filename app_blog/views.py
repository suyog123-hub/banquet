from django.shortcuts import render
from .models import content
from rest_framework.views import APIView
from config.permission import BasePermission
from config.pagination import Detailpage
from .serializer import Contentserializer
from rest_framework.response import Response
from rest_framework import status
from config.response import (
    success_response,
    error_response,
    server_error_response,
)
# Create your views here.

class contentView(APIView):
    pagination_class = Detailpage
    def get(self,request):
        value = content.objects.all().order_by('id')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(value, request)
        serializer = Contentserializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self,request):
        try:
            serializer = Contentserializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_response("data fetch successfully",serializer.data,200)
            return error_response(serializer.errors,400)
        except Exception as e:
            return Response({
                "message":str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

