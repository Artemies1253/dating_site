from django.urls import path
from src.user.views import UserList, CreateAvatar


urlpatterns = [
    path("list", UserList.as_view()),
    path("add_avatar", CreateAvatar.as_view()),
]
