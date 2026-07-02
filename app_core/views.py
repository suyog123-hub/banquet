from django.shortcuts import render
from rest_framework import viewsets
from .models import WeddingPalace
from .serializer import WeddingPalaceSerializer
from rest_framework.permissions import IsAdminUser
# Create your views here.
class organization_view(viewsets.ModelViewSet):
    queryset = WeddingPalace.objects.all()
    serializer_class = WeddingPalaceSerializer
    permission_classes = [IsAdminUser]
