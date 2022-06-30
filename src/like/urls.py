from django.urls import path

from src.like.api import CreateLikeAPIView, DeleteLikeAPIView, ListLikeAPIView

urlpatterns = [
    path("create", CreateLikeAPIView.as_view(), name='create_like'),
    path("<int:pk>", DeleteLikeAPIView.as_view(), name="delete_like"),
    path("list", ListLikeAPIView.as_view())
]
