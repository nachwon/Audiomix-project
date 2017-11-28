from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.nickname')

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'author',
            'master_track',
            'author_track',
        )
