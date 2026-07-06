from django.shortcuts import render
from .models import  Content , BlogCategory
from rest_framework.views import APIView 
from rest_framework import viewsets
from config.permission import BasePermission
from config.pagination import Detailpage
from .serializer import  Contentserializer, CategorySerializers  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from config.response import (
    success_response,
    error_response,
    server_error_response,
)

class CategoryView(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminUser]

class ContentView(APIView):
    pagination_class = Detailpage
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        try:
            value = Content.objects.all().order_by('id')
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(value, request)
            serializer = Contentserializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = Contentserializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return success_response(
                    "Content created successfully", 
                    serializer.data, 
                    201
                )
            return error_response(serializer.errors, 400)
            
        except Exception as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk): 
        try:
            content_instance = get_object_or_404(Content, id=pk)

            if content_instance.user != request.user:
                return Response({
                    'success': False,
                    'message': 'You are not authorized to edit this content'
                }, status=status.HTTP_403_FORBIDDEN)
            serializer =Contentserializer(content_instance, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Content updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """Delete a content (only author can delete)"""
        try:
            content_instance = get_object_or_404(Content, id=pk)

            if content_instance.user != request.user:
                return Response({
                    'success': False,
                    'message': 'You are not authorized to delete this content'
                }, status=status.HTTP_403_FORBIDDEN)
            content_instance.delete()
            
            return Response({
                'success': True,
                'message': 'Content deleted successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)