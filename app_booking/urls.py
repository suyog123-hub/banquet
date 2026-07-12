from django.urls import path
from .views import Bookingview
urlpatterns = [
    path("booking/",Bookingview.as_view(),name='booking'),
]
