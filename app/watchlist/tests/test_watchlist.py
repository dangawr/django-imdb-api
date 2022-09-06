from rest_framework.test import APITestCase
from django.urls import reverse
from watchlist.models import StreamPlatform, Watchlist
from django.contrib.auth.models import User
from rest_framework import status
from watchlist.serializers import WatchListSerializer

import tempfile
import os

from PIL import Image


WATCHLIST_URL = reverse('watchlist:movie-list')


def image_upload_url(recipe_id):
    return reverse('watchlist:upload-image', args=[recipe_id])


def movie_detail_url(pk):
    return reverse('watchlist:movie-detail', args=[pk])


class NormalUserTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_user',
            password='Test!23'
        )
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'Stream 1',
            'about': 'Some text',
            'website': 'http://test.com',
        }
        self.platform = StreamPlatform.objects.create(**payload)
        self.watch = Watchlist.objects.create(
            platform=self.platform,
            title="Example Movie",
            storyline="Example Movie",
            active=True
        )

    def test_watchlist_create(self):
        payload = {
            'title': 'test title 1',
            'storyline': 'test storyline',
            'active': True,
        }

        response = self.client.post(reverse('watchlist:movie-create', args=[self.platform.id]), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_watchlist_list(self):
        response = self.client.get(WATCHLIST_URL)
        watch = Watchlist.objects.all()
        serializer = WatchListSerializer(watch, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(movie_detail_url(self.watch.id))
        serializer = WatchListSerializer(self.watch)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Watchlist.objects.count(), 1)
        self.assertEqual(Watchlist.objects.get().title, 'Example Movie')
        self.assertEqual(response.data, serializer.data)


class ImageUploadTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'user@example.com',
            'password123',
        )
        self.client.force_authenticate(self.user)
        payload = {
            'name': 'Stream 1',
            'about': 'Some text',
            'website': 'http://test.com',
        }
        self.platform = StreamPlatform.objects.create(**payload)
        self.watch = Watchlist.objects.create(
            platform=self.platform,
            title="Example Movie",
            storyline="Example Movie",
            active=True
        )

    def tearDown(self):
        self.watch.image.delete()

    def test_upload_image(self):
        url = image_upload_url(self.watch.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.watch.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.watch.image.path))

    def test_upload_image_bad_request(self):
        url = image_upload_url(self.watch.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
