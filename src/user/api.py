from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.authorization.services import create_token
from src.base.permissions import IsAuthor
from src.base.services import get_border_coordinates
from src.user.filters import UserListFilter
from src.user.models import User, Avatar, UserImage
from src.user.serializer import UserDetailListSerializer, UserDetailSerializer, UserUpdateSerializer, \
     AvatarSerializer, ImageSerializer


class UserList(generics.ListAPIView):
    serializer_class = UserDetailListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserListFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(is_delete=False, is_admin=False).exclude(id=user.id)
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
    queryset = User.objects.filter(is_delete=False, is_admin=False)


class UserSelfAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserUpdateSerializer

    def get_object(self):
        user_id = self.request.user.id
        obj = User.objects.get(id=user_id)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateAvatar(generics.CreateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)


class DeleteAvatar(generics.DestroyAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthor]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active:
            last_avatar = Avatar.objects.filter(user=request.user).last()  # TODO: вынести в сервисы
            last_avatar.is_active = True
            last_avatar.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateImage(generics.CreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)


class DeleteImage(generics.DestroyAPIView):
    queryset = UserImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthor]
