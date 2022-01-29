from django.urls import path

from src.user.views import CreateLike

urlpatterns = [
    path("create", CreateLike.as_view())
]
