from rest_framework import serializers
from .models import Watch, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watch',)
        read_only_fields = ['id']


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source="platform.name", read_only=True)
    # platform = serializers.StringRelatedField()  # in this case, the same display as above /\

    class Meta:
        model = Watch
        fields = "__all__"
        read_only_fields = ['id', 'avg_rating', 'ratings_number']


class StreamPlatformSerializer(serializers.ModelSerializer):
    watch = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        read_only_fields = ['id']
