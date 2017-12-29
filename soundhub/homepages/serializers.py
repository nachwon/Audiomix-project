from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post
from utils.fields import BypassEmptyStringField, AuthorField

User = get_user_model()


class HomepagePostSerializer(serializers.ModelSerializer):
    author = AuthorField(read_only=True)
    post_img = BypassEmptyStringField(use_url=False)
    author_track = serializers.FileField(max_length=255, use_url=False, required=False)
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


class HomePageUserSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(read_only=True, use_url=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nickname',
            'profile_img',
            'instrument',
            'user_type',
            'genre',
            'total_liked',
            'num_followings',
            'num_followers',
            'is_active',
            'last_login',
        )
