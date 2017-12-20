from rest_framework import serializers

from posts.models import Post
from utils.fields import BypassEmptyStringField


class HomepagePostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    post_img = BypassEmptyStringField(use_url=False)
    author_track = serializers.FileField(max_length=255, use_url=False, required=False)
    liked = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    master_track = serializers.FileField(max_length=255, use_url=False, required=False)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'author',
            'post_img',
            'instrument',
            'genre',
            'num_liked',
            'num_comments',
            'created_date',
            'master_track',
            'author_track',
        )
