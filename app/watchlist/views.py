from django.shortcuts import render
from watchlist.models import WatchList
from django.http import JsonResponse


def movie_list(request):
    movies = WatchList.objects.all()
    data = {
        'movies': list(movies.values())
    }
    return JsonResponse(data)


def movie_details(request, pk):
    movie = WatchList.objects.get(pk=pk)
    data = {
        'name': movie.name,
        'description': movie.description,
        'active': movie.active
    }
    return JsonResponse(data)
