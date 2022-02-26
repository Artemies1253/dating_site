from rest_framework import serializers

from src.notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = 'is_unread', 'message', 'like'


