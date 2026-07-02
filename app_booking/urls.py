from django.urls import path
from .views import Bookingview
urlpatterns = [
    path("",Bookingview.as_view(),name='booking'),
]
