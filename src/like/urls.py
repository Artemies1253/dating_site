from django.urls import path

from src.like.views import CreateLike

urlpatterns = [
    path("create", CreateLike.as_view())
]
