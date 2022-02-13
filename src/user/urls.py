from django.urls import path
from src.user.views import UserList, CreateAvatar, DeleteAvatar, CreateImage, DeleteImage

urlpatterns = [
    path("list", UserList.as_view()),
    path("add_avatar", CreateAvatar.as_view()),
    path("add_image", CreateImage.as_view()),
    path("delete_avatar/<int:pk>", DeleteAvatar.as_view()),
    path("delete_image/<int:pk>", DeleteImage.as_view()),
]
