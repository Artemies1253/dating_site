import datetime
import json

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from src.like.models import Like
from src.user.models import User


class TestLikeView(APITestCase):
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
        self.like = Like.objects.create(owner_user=self.user1, liked_user=self.user2)

    def test_create_like(self):
        url = reverse('create_like')
        data = {
            'owner_user': self.user1.id,
            'liked_user': self.user3.id,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user1)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data, response.data)

    def test_delete_like(self):
        url = reverse("delete_like", kwargs={"pk": 1})
        self.client.force_authenticate(self.user1)
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(None, response.data)

    def test_delete_permission_denied(self):
        url = reverse("delete_like", kwargs={"pk": 1})
        self.client.force_authenticate(self.user3)
        response = self.client.delete(url, content_type='application/json')
        error = {
            'detail': ErrorDetail(
                string='You do not have permission to perform this action.', code='permission_denied'
            )
        }
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(error, response.data)
