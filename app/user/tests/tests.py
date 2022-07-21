from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


CREATE_USER_URL = reverse('user:register')
TOKEN_URL = reverse('user:token')
LOGOUT_URL = reverse('user:logout')


class PublicUserApiTests(APITestCase):

    def test_register(self):
        payload = {
            'username': 'testcase',
            'email': 'testcase@example.com',
            'password': 'test123',
            'password2': 'test123',
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginUserApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testcase', password='test123')

    def test_login(self):
        payload = {
            'username': 'testcase',
            'password': 'test123',
        }
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(LOGOUT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

