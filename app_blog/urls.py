from django.urls import path,include
from .views import ContentView , CategoryView , CommentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("category",CategoryView,basename="category")
urlpatterns = [
    path("content/",ContentView.as_view(),name="content"),
    path("content/<int:pk>/",ContentView.as_view(),name="content1"),
    path("comment/",CommentView.as_view(),name="comment"),
    path("",include(router.urls))
]
