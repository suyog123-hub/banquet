from django.urls import path
from .views import contentView
urlpatterns = [
    path("content/",contentView.as_view(),name="content"),
]
