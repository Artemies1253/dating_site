from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response

from src.authorization.services import create_token
from src.base.permission import IsOwnerUserPermission
from src.base.services import get_border_coordinates
from src.user.filters import UserListFilter
from src.user.models import User
from src.user.serializer import UserDetailListSerializer, UserDetailSerializer, UserUpdateSerializer, UserInfoSerializer


class UserList(generics.ListAPIView):
    serializer_class = UserDetailListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserListFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = User.objects.filter(is_delete=False)
        user = self.request.user
        longitude = user.longitude
        latitude = user.latitude
        distance = self.request.query_params.get("distance")
        if distance:
            distance = int(distance)
            border_coordinates = get_border_coordinates(longitude, latitude, distance)
            queryset = User.objects.filter(
                longitude__lte=border_coordinates['max_longitude'],
                longitude__gte=border_coordinates['min_longitude'],
                latitude__lte=border_coordinates['max_latitude'],
                latitude__gte=border_coordinates['min_latitude'],
            ).exclude(id=user.id)
        gender = self.request.query_params.get("gender")
        if gender:
            queryset = queryset.filter(gender=gender)
        return queryset


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.filter(is_delete=False)


class UserAPIView(generics.GenericAPIView):
    permissions = (IsOwnerUserPermission,)

    def get(self, request):
        serializer = UserInfoSerializer(self.request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserUpdateSerializer(data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            user = serializer.update(instance=self.request.user, validated_data=serializer.validated_data)
            user_detail = UserInfoSerializer(user)
            return Response(user_detail.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = self.request.user
        user.is_delete = True
        user.save()
        create_token(user_id=user.id)

        return Response(status=status.HTTP_204_NO_CONTENT)
