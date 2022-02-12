from urllib import request
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

from src.base.services import get_border_coordinates
from src.user.filters import UserListFilter
from src.user.models import User
from src.user.serializer import UserDetailSerializer


class UserList(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserListFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = User.object.all()
        user = self.request.user
        longitude = user.longitude
        latitude = user.latitude
        distance = self.request.query_params.get("distance")
        if distance:
            distance = int(distance)
            border_coordinates = get_border_coordinates(longitude, latitude, distance)
            queryset = User.object.filter(
                longitude__lte=border_coordinates['max_longitude'],
                longitude__gte=border_coordinates['min_longitude'],
                latitude__lte=border_coordinates['max_latitude'],
                latitude__gte=border_coordinates['min_latitude'],
                ).exclude(id=user.id)
        gender = self.request.query_params.get("gender")
        if gender:
            queryset = queryset.filter(gender=gender)
        return queryset



