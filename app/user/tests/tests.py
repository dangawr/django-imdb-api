from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


CREATE_USER_URL = reverse('user:register')
TOKEN_URL = reverse('user:token')
LOGOUT_URL = reverse('user:logout')
ME_URL = reverse('user:me')


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


class RegisteredUserApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testcase',
            password='test123',
            email='test123@example.com',
        )

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

    def test_password_reset(self):
        response = self.client.post(reverse('password_reset:reset-password-request'), {'email': self.user.email})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user_data(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            'username': 'another_username',
            'password': 'another_password',
        }
        response = self.client.patch(ME_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(payload.get('username'), self.user.username)


