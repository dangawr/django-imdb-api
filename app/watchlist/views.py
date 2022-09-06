from .models import Watchlist, StreamPlatform, Review
from .serializers import (
    WatchListSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
    WatchlistUploadImageSerializer
    )
from rest_framework import generics, viewsets, status, parsers
from rest_framework.exceptions import ValidationError
from .permissions import IsReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .paginnation import WatchListPagination
from rest_framework.response import Response


class ReviewCreateView(generics.CreateAPIView):
    """View for review creating."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = Watchlist.objects.get(pk=pk)
        user = self.request.user
        user_review = Review.objects.filter(
            watchlist=watchlist,
            review_user=user
        )

        if user_review.exists():
            raise ValidationError("You have commented this Title!")

        if watchlist.avg_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2

        watchlist.ratings_number += 1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage for reviews in database."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]


class ReviewView(generics.ListAPIView):
    """Manage for reviews in database."""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class StreamPlatformViewSet(viewsets.ModelViewSet):
    """View for manage stream platforms."""
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAuthenticated]


class WatchListView(generics.ListAPIView):
    """View for list or create watchlist."""
    queryset = Watchlist.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'platform__name']
    pagination_class = WatchListPagination


class WatchListCreateApiView(generics.CreateAPIView):
    """View for tittle creating. Please pass the stream platform ID"""
    serializer_class = WatchListSerializer

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        stream_platform = StreamPlatform.objects.get(pk=pk)
        serializer.save(platform=stream_platform)


class WatchListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Title details view."""
    queryset = Watchlist.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [IsAuthenticated]


class WatchlistUploadImageApiView(generics.GenericAPIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    serializer_class = WatchlistUploadImageSerializer

    def post(self, request, pk):
        watchlist = Watchlist.objects.get(pk=pk)
        serializer = self.serializer_class(instance=watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

