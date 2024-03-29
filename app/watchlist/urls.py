from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'watchlist'


router = DefaultRouter()

router.register('stream', views.StreamPlatformViewSet, basename='stream')

urlpatterns = [
    path('list/', views.WatchListView.as_view(), name='movie-list'),
    path('<int:pk>/', views.WatchListDetailView.as_view(), name='movie-detail'),
    path('<int:pk>/upload-image/', views.WatchlistUploadImageApiView.as_view(), name='upload-image'),
    path('stream/<int:pk>/title-create/', views.WatchListCreateApiView.as_view(), name='movie-create'),
    path('<int:pk>/reviews/', views.ReviewView.as_view(), name='review-list'),
    path('review/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('<int:pk>/review-create/', views.ReviewCreateView.as_view(), name='review-create'),

    path('', include(router.urls)),
]
