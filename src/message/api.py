from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from src.base.permissions import IsAuthor
from src.base.services import create_notification
from src.message.models import Message
from src.message.serializers import MessageCreateSerializer, MessageListSerializer, MessageUpdateOrDeleteSerializer


class MessageListView(generics.ListAPIView):
    """Отобразить список всех сообщений с пользователем {id}"""
    serializer_class = MessageListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        author = self.request.user
        receiver_id = self.request.resolver_match.kwargs['pk']
        queryset = Message.objects.filter(
            Q(author=author, receiver=receiver_id) |
            Q(author=receiver_id, receiver=author)
        )
        return queryset


class MessageCreate(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        message = serializer.save(author=self.request.user)
        create_notification(instance=message, user=message.receiver)


class MessageUpdateOrDelete(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthor]
    serializer_class = MessageUpdateOrDeleteSerializer

    def get_object(self):
        author = self.request.user
        message_id = self.request.resolver_match.kwargs['message_id']
        message = Message.objects.get(author=author, id=message_id)
        return message
