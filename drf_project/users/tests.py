from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import UM


class UserDetailTestCase(TestCase):
    def setUp(self):
        self.user = UM.objects.create_user(username='test_user', password='test_password')
        self.client = APIClient()

    def test_user_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], self.user.username)

    def test_user_detail_unauthenticated(self):
        url = reverse('user-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)