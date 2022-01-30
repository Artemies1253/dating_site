from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from src.user.filters import UserListFilter
from src.user.models import User
from src.user.serializer import UserDetailSerializer


class UserList(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.object.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserListFilter


