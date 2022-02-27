from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from src.notification.models import Notification
from src.notification.serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(is_unread=True, user=user)[::1]
        Notification.objects.update(is_unread=False)

        return queryset
