from django.urls import path
from .views import contactview

urlpatterns = [
    path('',contactview.as_view(),name='contact'),
     path('<int:id>/',contactview.as_view(),name='contact'),
]

