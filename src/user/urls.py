from django.urls import path
from src.user.api import UserList, UserDetailAPIView, UserAPIView

urlpatterns = [
    path("list", UserList.as_view()),
    path("detail/<int:pk>", UserDetailAPIView.as_view()),
    path("self", UserAPIView.as_view()),
]
