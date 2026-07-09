# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import organization_view

router = DefaultRouter()
router.register('organization', organization_view, basename='palace')

urlpatterns = [
    path('', include(router.urls)),
]