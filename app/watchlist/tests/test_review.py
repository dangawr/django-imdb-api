from rest_framework.test import APITestCase
from django.urls import reverse
from watchlist.models import StreamPlatform, Watch
from django.contrib.auth.models import User
from rest_framework import status


def review_create_url(watchlist_pk):
    return reverse('watchlist:review-create', args=[watchlist_pk])


def review_detail_url(review_pk):
    return reverse('watchlist:review-detail', args=[review_pk])


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

    def test_review_create(self):
        payload = {
            "rating": 5,
            "description": "Great Movie!",
            "active": True
        }

        response = self.client.post(review_create_url(self.watch.id), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

