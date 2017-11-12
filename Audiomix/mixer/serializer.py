from rest_framework import serializers

from mixer.models import Post, Commit


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = (
            'author',
            'instrument',
            'commit',
        )


class PostSerializer(serializers.ModelSerializer):
    commits = CommitSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'track',
            'commits',
        )