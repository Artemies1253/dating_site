from django.urls import path

from src.like.api import CreateLike

urlpatterns = [
    path("create", CreateLike.as_view())
]
