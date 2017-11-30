from rest_framework import serializers

from posts.models import Post, CommentTrack
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    # 유저 시리얼라이저를 통해 유저 객체 직렬화 후 할당
    author = UserSerializer(read_only=True)
    author_track = serializers.FileField(max_length=255, use_url=False)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'author',
            'master_track',
            'author_track',
            'comment_tracks',
        )

        depth = 1


class CommentTrackSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='nickname'
    )
    post = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title',
    )

    class Meta:
        model = CommentTrack
        fields = (
            'id',
            'author',
            'post',
            'comment_track',
            'instrument',
        )
