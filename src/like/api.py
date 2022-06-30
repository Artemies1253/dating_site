from rest_framework import generics, mixins, status
from rest_framework import permissions
from rest_framework.response import Response

from src.base.permissions import IsOwnerLike
from src.like.models import Like
from src.like.serializer import CreateLikeSerializer, LikeDetailSerializer


class CreateLikeAPIView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = CreateLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data.copy()
        data["owner_user"] = self.request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteLikeAPIView(generics.DestroyAPIView):
    serializer_class = CreateLikeSerializer
    permission_classes = (IsOwnerLike,)
    queryset = Like.objects.all()


class ListLikeAPIView(generics.GenericAPIView):
    serializer_class = LikeDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        owner_like_list = Like.objects.filter(owner_user=user)
        liked_user_list = Like.objects.filter(liked_user=user)
        data = {
            "owner_like_list": self.serializer_class(instance=owner_like_list, many=True).data,
            "liked_user_list": self.serializer_class(instance=liked_user_list, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)
