from django.urls import path
from .views import contactview

urlpatterns = [
    path('contact/',contactview.as_view(),name='contact'),
]

