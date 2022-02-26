from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions

from src.base.services import create_notification
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
            like, like_status = serializer.save()
            liked_user = User.objects.get(id=serializer.validated_data.get("liked_user_id"))
            create_notification(instance=like, user=liked_user)
            from_like_user = request.user

            if like_status:
                if is_mutual_like(from_like_user, liked_user):
                    send_email_of_like(from_like_user, liked_user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
