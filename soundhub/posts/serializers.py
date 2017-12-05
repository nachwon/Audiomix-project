from rest_framework import serializers

from posts.models import Post, CommentTrack
from users.serializers import UserSerializer


class CommentTrackSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='nickname'
    )
    post = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title',
    )
    comment_track = serializers.FileField(max_length=255, use_url=False)

    class Meta:
        model = CommentTrack
        fields = (
            'id',
            'author',
            'post',
            'comment_track',
            'instrument',
        )


class PostListSerializer(serializers.ModelSerializer):
    # 유저 시리얼라이저를 통해 유저 객체 직렬화 후 할당
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='nickname'
    )
    author_track = serializers.FileField(max_length=255, use_url=False)
    liked = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'author',
            'instrument',
            'genre',
            'liked',
            'num_liked',
            'created_date',
            'master_track',
            'author_track',
        )


class CommentTrackField(serializers.RelatedField):
    def to_representation(self, value):
        vocal_list = list()
        guitar_list = list()
        bass_list = list()
        drums_list = list()
        keys_list = list()
        others_list = list()

        data = dict()
        for i in value.all():
            list_item = CommentTrackSerializer(i).data
            if i.instrument in ('Bass', 'B'):
                bass_list.append(list_item)
                data['Bass'] = bass_list
            elif i.instrument in ('Vocal', 'V'):
                vocal_list.append(list_item)
                data['Vocal'] = vocal_list
            elif i.instrument in ('Guitar', 'G'):
                guitar_list.append(list_item)
            elif i.instrument in ('Drums', 'D'):
                drums_list.append(list_item)
                data['Drums'] = drums_list
            elif i.instrument in ('Keyboard', 'K'):
                keys_list.append(list_item)
                data['Keyboard'] = keys_list
            elif i.instrument in ('Others', 'O'):
                others_list.append(list_item)
                data['Others'] = others_list
        return data


class PostDetailSerializer(serializers.ModelSerializer):
    # 유저 시리얼라이저를 통해 유저 객체 직렬화 후 할당
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='nickname'
    )
    author_track = serializers.FileField(max_length=255, use_url=False)
    liked = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comment_tracks = CommentTrackField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'author',
            'instrument',
            'genre',
            'liked',
            'num_liked',
            'created_date',
            'master_track',
            'author_track',
            'comment_tracks',
        )
