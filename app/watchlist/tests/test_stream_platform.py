from rest_framework.test import APITestCase
from django.urls import reverse
from watchlist.models import StreamPlatform
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


STREAM_URL = reverse('watchlist:stream-list')


def stream_detail_url(pk):
    return reverse('watchlist:stream-detail', args=[pk])


class NormalUserTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test_user', password='Test!23')
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'Stream 1',
            'about': 'Some text',
            'website': 'http://test.com',
        }
        self.platform = StreamPlatform.objects.create(**payload)

    def test_stream_platform_create(self):

        payload = {
            'name': 'Stream 2',
            'about': 'Some text',
            'website': 'http://test.com'
        }
        response = self.client.post(STREAM_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_list(self):

        response = self.client.get(STREAM_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_platform_retrieve(self):

        pk = self.platform.id
        response = self.client.get(stream_detail_url(pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_platform_delete(self):

        pk = self.platform.id
        response = self.client.delete(stream_detail_url(pk))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_patch(self):

        payload = {
            'about': 'edited text',
        }

        pk = self.platform.id
        response = self.client.patch(stream_detail_url(pk), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
