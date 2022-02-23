import json

from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.message.models import Message
from src.message.serializers import MessageListSerializer
from src.user.models import User


class TestMessageListView(APITestCase):
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

        self.count_message = Message.objects.all().count()

    def test_message_list_ok(self):
        self.client.force_authenticate(self.user1)
        url = reverse('message_list', args=(self.user2.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        messages = Message.objects.filter(
            Q(author=self.user1, receiver=self.user2) |
            Q(author=self.user2, receiver=self.user1)
        )
        serializer_data = MessageListSerializer(messages, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_message_list_not_authenticated(self):
        url = reverse('message_list', args=(self.user2.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_message_create(self):
        self.assertEqual(self.count_message, Message.objects.all().count())
        url = reverse('message_create')
        data = {
            'receiver': self.user2.id,
            'text': 'Hello123',
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user1)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data, response.data)
        self.assertEqual(self.count_message + 1, Message.objects.all().count())

    def test_message_create_not_authenticated(self):
        self.assertEqual(self.count_message, Message.objects.all().count())
        url = reverse('message_create')
        data = {
            'receiver': self.user2.id,
            'text': 'Hello123',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(self.count_message, Message.objects.all().count())

    def test_message_update(self):
        url = reverse('message_update_or_delete', args=(self.message1.id,))
        data = {
            'text': 'Hello, dear!',
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user1)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.message1.refresh_from_db()
        self.assertEqual(data['text'], self.message1.text)

    def test_message_delete(self):
        self.assertTrue(self.message1)
        self.assertEqual(self.count_message, Message.objects.all().count())
        url = reverse('message_update_or_delete', args=(self.message1.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Message.objects.filter(id=self.message1.id).exists())
        self.assertEqual(self.count_message - 1, Message.objects.all().count())

    def test_message_delete_not_authenticated(self):
        self.assertEqual(self.count_message, Message.objects.all().count())
        url = reverse('message_update_or_delete', args=(self.message1.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(self.count_message, Message.objects.all().count())
