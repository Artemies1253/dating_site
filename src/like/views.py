from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions

from src.like.serializer import CreateLikeSerializer
from src.like.service import is_mutual_like, send_email_of_like
from src.user.models import User


class CreateLike(generics.GenericAPIView):
    serializer_class = CreateLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request_data = request.data.copy()
        request_data["from_like_user_id"] = request.user.id
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid(raise_exception=True):
            like = serializer.save()
            liked_user = User.object.get(id=serializer.validated_data.get("liked_user_id"))
            from_like_user = request.user

            if like[1]:
                if is_mutual_like(from_like_user, liked_user):
                    send_email_of_like(from_like_user, liked_user)

            like = like[0]
            return Response({"id": like.id}, status=status.HTTP_201_CREATED)
