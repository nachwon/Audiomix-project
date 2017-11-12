from rest_framework import serializers

from mixer.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'track',
        )