from watchlist import models
from django.test import TestCase


class ModelTest(TestCase):

    def test_create_movie(self):
        movie = models.WatchList.objects.create(
            title='Test Name',
            storyline='Test Description',
        )

        self.assertEqual(str(movie), movie.title)
