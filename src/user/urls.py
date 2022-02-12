from django.urls import path
from src.user.views import UserList


urlpatterns = [
    path("list", UserList.as_view()),
]
