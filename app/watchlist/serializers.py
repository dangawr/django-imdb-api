from rest_framework import serializers
from .models import WatchList, StreamPlatform


class WatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = ['id', 'title', 'storyline', 'created']
        read_only_fields = ['id']


class StreamPlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        read_only_fields = ['id']
