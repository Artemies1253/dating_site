import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.like.models import Like
from src.message.models import Message
from src.notification.models import Notification
from src.notification.serializers import NotificationSerializer
from src.user.models import User


class TestNotificationListView(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='user1@mail.com', first_name='Vasya', last_name='1',
                                         gender='m', avatar='avatar/2/watermark_dtT2d8y.jpg',
                                         address='some_address1', latitude=101, longitude=101)
        self.user2 = User.objects.create(email='user2@mail.com', first_name='Petya', last_name='2',
                                         gender='m', avatar='avatar/2/watermark_dtT2d8.jpg',
                                         address='some_address2', latitude=102, longitude=102)
        self.user3 = User.objects.create(email='user3@mail.com', first_name='Kolya', last_name='3',
                                         gender='m', avatar='avatar/2/watermark_dtT2d7.jpg',
                                         address='some_address3', latitude=103, longitude=103)

        self.message1 = Message.objects.create(author=self.user1, receiver=self.user2, text='Hello')
        self.message2 = Message.objects.create(author=self.user2, receiver=self.user1, text='how are you?')

        self.like1 = Like.objects.create(owner_user=self.user1, liked_user=self.user2)

        self.notification = Notification.objects.create(message=self.message1, user=self.user1)
        self.notification = Notification.objects.create(like=self.like1, user=self.user1)

        self.count_notification = Notification.objects.all().count()

    def test_notification_list(self):
        url = reverse('notification_list')
        self.client.force_authenticate(self.user1)
        notifications = Notification.objects.filter(is_unread=True, user=self.user1)
        self.assertTrue(notifications)
        serializer_data = NotificationSerializer(notifications, many=True).data
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_notification_create_for_message(self):
        self.assertEqual(self.count_notification, Notification.objects.all().count())
        url = reverse('message_create')
        data = {
            'receiver': self.user2.id,
            'text': 'Hello123',
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user1)
        response = self.client.post(url, data=json_data, content_type='application/json')
        message_id = Message.objects.last().id
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        created_notification = Notification.objects.last()
        serializer_data = NotificationSerializer(created_notification).data
        notification_data = {
            'message': message_id,
            'like': None,
            'is_unread': True,
        }
        self.assertEqual(notification_data, serializer_data)
        self.assertEqual(self.count_notification + 1, Notification.objects.all().count())

    def test_notification_create_for_like(self):
        self.assertEqual(self.count_notification, Notification.objects.all().count())
        url = reverse('create_like')
        data = {
            'liked_user': self.user3.id,
            'owner_user': self.user1.id,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user1)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        like_id = Like.objects.last().id
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        created_notification = Notification.objects.last()
        serializer_data = NotificationSerializer(created_notification).data
        notification_data = {
            'message': None,
            'like': like_id,
            'is_unread': True,
        }
        self.assertEqual(notification_data, serializer_data)
        self.assertEqual(self.count_notification + 1, Notification.objects.all().count())