from rest_framework.test import APITestCase

from src.message.models import Message
from src.message.serializers import MessageListSerializer, MessageCreateSerializer, MessageUpdateOrDeleteSerializer
from src.user.models import User


class TestMessageSerializer(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='user1@mail.com', first_name='Vasya', last_name='1',
                                         gender='m', avatar='avatar/2/watermark_dtT2d8y.jpg',
                                         address='some_address1', latitude=101, longitude=101)
        self.user2 = User.objects.create(email='user2@mail.com', first_name='Petya', last_name='2',
                                         gender='m', avatar='avatar/2/watermark_dtT2d8.jpg',
                                         address='some_address2', latitude=102, longitude=102)

        self.message1 = Message.objects.create(author=self.user1, receiver=self.user2, text='Hello')
        self.message2 = Message.objects.create(author=self.user2, receiver=self.user1, text='how are you?')

    def test_message_list_serializer_ok(self):
        messages = Message.objects.all()
        data = MessageListSerializer(messages, many=True).data
        expected_data = [
            {
                'id': 1,
                'text': 'Hello',
                'created_at': data[0]['created_at'],
                'updated_at': data[0]['updated_at'],
                'is_updated': False,
                'author': 1,
                'receiver': 2
            },
            {
                'id': 2,
                'text': 'how are you?',
                'created_at': data[1]['created_at'],
                'updated_at': data[1]['updated_at'],
                'is_updated': False,
                'author': 2,
                'receiver': 1
            }
        ]
        self.assertEqual(expected_data, data)

    def test_message_create_serializer(self):
        new_message = Message.objects.get(id=self.message1.id)
        data = MessageCreateSerializer(new_message).data
        expected_data = {
            'text': 'Hello',
            'receiver': 2,
        }
        self.assertEqual(expected_data, data)

    def test_message_update_or_delete_serializer(self):
        new_message = Message.objects.get(id=self.message1.id)
        data = MessageUpdateOrDeleteSerializer(new_message).data
        expected_data = {
            'text': 'Hello',
        }
        self.assertEqual(expected_data, data)