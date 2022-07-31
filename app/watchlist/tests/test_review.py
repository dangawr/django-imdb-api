from rest_framework.test import APITestCase
from django.urls import reverse
from watchlist.models import StreamPlatform, Watchlist, Review
from django.contrib.auth.models import User
from rest_framework import status
from watchlist.serializers import ReviewSerializer


def review_list_url(watchlist_pk):
    return reverse('watchlist:review-list', args=[watchlist_pk])


def review_create_url(watchlist_pk):
    return reverse('watchlist:review-create', args=[watchlist_pk])


def review_detail_url(review_pk):
    return reverse('watchlist:review-detail', args=[review_pk])


class UnAuthUserTests(APITestCase):

    def setUp(self) -> None:
        payload = {
            'name': 'Stream 1',
            'about': 'Some text',
            'website': 'http://test.com',
        }
        self.platform = StreamPlatform.objects.create(**payload)
        self.watchlist = Watchlist.objects.create(
            platform=self.platform,
            title="Example Movie",
            storyline="Example Movie",
            active=True
        )

    def test_review_create(self):
        payload = {
            "rating": 5,
            "description": "Great Movie!",
            "active": True
        }

        response = self.client.post(review_create_url(self.watchlist.id), payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
        self.watch = Watchlist.objects.create(
            platform=self.platform,
            title="Example Movie",
            storyline="Example Movie",
            active=True
        )

    def test_review_list(self):
        payload = {
            "rating": 5,
            "description": "Great Movie!",
            "active": True,
            "watchlist": self.watch,
            "review_user": self.user,
        }
        Review.objects.create(**payload)
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        response = self.client.get(review_list_url(self.watch.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_review_create(self):
        payload = {
            "rating": 5,
            "description": "Great Movie!",
            "active": True
        }

        response = self.client.post(review_create_url(self.watch.id), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        review = Review.objects.get(pk=response.data['id'])
        self.assertEqual(review.review_user, self.user)

        for k, v in payload.items():
            self.assertEqual(getattr(review, k), v)

    def test_review_update(self):
        payload = {
            "rating": 5,
            "description": "Great Movie!",
            "active": True,
            "watchlist": self.watch,
            "review_user": self.user,
        }
        review = Review.objects.create(**payload)

        new_data = {
            "rating": 4,
            "description": "Updated!",
            "active": True
        }
        response = self.client.put(review_detail_url(review.id), new_data)

        review.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in new_data.items():
            self.assertEqual(getattr(review, k), v)

    def test_review_delete(self):
        payload = {
            "rating": 5,
            "description": "Great Movie!",
            "active": True,
            "watchlist": self.watch,
            "review_user": self.user,
        }
        review = Review.objects.create(**payload)

        response = self.client.delete(review_detail_url(review.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



