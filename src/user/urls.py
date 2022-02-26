from django.urls import path
from src.user.api import UserList, UserDetailAPIView, CreateAvatar, DeleteAvatar, CreateImage, DeleteImage, \
    UserSelfAPIView

urlpatterns = [
    path("list", UserList.as_view(), name='user_list'),
    path("add_avatar", CreateAvatar.as_view()),
    path("add_image", CreateImage.as_view()),
    path("delete_avatar/<int:pk>", DeleteAvatar.as_view()),
    path("delete_image/<int:pk>", DeleteImage.as_view()),
    path("<int:pk>", UserDetailAPIView.as_view(), name='user_detail'),
    path("self", UserSelfAPIView.as_view(), name='user_self'),
]
