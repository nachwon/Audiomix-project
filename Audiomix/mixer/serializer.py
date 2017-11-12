from rest_framework import serializers

from mixer.models import Post, Commit


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'track',
        )


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = (
            'id',
            'author',
            'post',
            'instrument',
            'commit',
        )
