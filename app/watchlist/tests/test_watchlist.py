from rest_framework.test import APITestCase
from django.urls import reverse
from watchlist.models import StreamPlatform, Watch
from django.contrib.auth.models import User
from rest_framework import status
from watchlist.serializers import WatchListSerializer


WATCHLIST_URL = reverse('watchlist:movie-list')


def movie_detail_url(pk):
    return reverse('watchlist:movie-detail', args=[pk])


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
        self.watch = Watch.objects.create(platform=self.platform, title="Example Movie",
                                          storyline="Example Movie", active=True)

    def test_watchlist_create(self):
        payload = {
            'title': 'test title 1',
            'storyline': 'test storyline',
            'active': True,
            'platform': self.platform,
        }

        response = self.client.post(WATCHLIST_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(WATCHLIST_URL)
        watch = Watch.objects.all()
        serializer = WatchListSerializer(watch, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(movie_detail_url(self.watch.id))
        serializer = WatchListSerializer(self.watch)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Watch.objects.count(), 1)
        self.assertEqual(Watch.objects.get().title, 'Example Movie')
        self.assertEqual(response.data, serializer.data)
