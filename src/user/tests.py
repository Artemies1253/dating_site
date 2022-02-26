from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.base.services import get_border_coordinates
from src.user.models import User
from src.user.serializer import UserDetailListSerializer, UserDetailSerializer, UserUpdateSerializer


class TestUser(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email='user1@mail.com', first_name='Vasya', last_name='1', gender='m',
            avatar=None, address='some_address1', latitude=55.851312, longitude=37.499812
        )
        self.user2 = User.objects.create(
            email='user2@mail.com', first_name='Petya', last_name='2', gender='m',
            avatar=None, address='some_address2', latitude=55.851308, longitude=37.499848,
            hobby='some_hobby', about_myself='some_info', status_text='my status', favorite_quotes='some_quotes',
            purpose_relationship='somebody'
        )
        self.user3 = User.objects.create(
            email='user3@mail.com', first_name='Kolya', last_name='3', gender='m',
            avatar=None, address='some_address3', latitude=103, longitude=103
        )
        self.user10 = User.objects.create(
            email='user10@mail.com', first_name='10_km_from_user1', last_name='10', gender='m',
            avatar=None, address='some_address_10km', latitude=55.931263, longitude=37.651978)

    def test_user_list_ok(self):
        url = reverse('user_list')
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user_data = User.objects.all().exclude(id=self.user1.id)
        serializer_data = UserDetailListSerializer(user_data, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_user_list_1km(self):
        url = reverse('user_list')
        self.client.force_authenticate(self.user1)
        response = self.client.get(url, {'distance': '1'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        border_coordinates = get_border_coordinates(self.user1.longitude, self.user1.latitude, distance=1)
        user_data = User.objects.filter(
                longitude__lte=border_coordinates['max_longitude'],
                longitude__gte=border_coordinates['min_longitude'],
                latitude__lte=border_coordinates['max_latitude'],
                latitude__gte=border_coordinates['min_latitude'],
            ).exclude(id=self.user1.id)
        serializer_data = UserDetailListSerializer(user_data, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_user_list_10km(self):
        url = reverse('user_list')
        self.client.force_authenticate(self.user1)
        response = self.client.get(url, {'distance': '10'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        border_coordinates = get_border_coordinates(self.user1.longitude, self.user1.latitude, distance=10)
        user_data = User.objects.filter(
                longitude__lte=border_coordinates['max_longitude'],
                longitude__gte=border_coordinates['min_longitude'],
                latitude__lte=border_coordinates['max_latitude'],
                latitude__gte=border_coordinates['min_latitude'],
            ).exclude(id=self.user1.id)
        serializer_data = UserDetailListSerializer(user_data, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_user_detail(self):
        url = reverse('user_detail', args='2')
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user_data = User.objects.get(id=self.user2.id)
        serializer_data = UserDetailSerializer(user_data).data
        self.assertEqual(serializer_data, response.data)

    def test_user_self_retrieve(self):
        url = reverse('user_self')
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user_data = User.objects.get(id=self.user2.id)
        serializer_data = UserUpdateSerializer(user_data).data
        self.assertEqual(serializer_data, response.data)

    def test_user_self_update(self):
        url = reverse('user_self')
        self.client.force_authenticate(self.user2)
        update_data = {
            'hobby': 'new_hobby'
        }
        response = self.client.patch(url, data=update_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user_data = User.objects.get(id=self.user2.id)
        serializer_data = UserUpdateSerializer(user_data).data
        self.assertEqual(serializer_data['hobby'], response.data['hobby'])

    def test_user_self_delete(self):
        url = reverse('user_self')
        self.client.force_authenticate(self.user2)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        user_data = User.objects.get(id=self.user2.id)
        self.assertIsNone(response.data)
        self.assertTrue(user_data.is_delete)
