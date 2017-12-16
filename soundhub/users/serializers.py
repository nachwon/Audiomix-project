import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class PostListField(serializers.RelatedField):
    def to_representation(self, value):
        post_list = value.all()
        data_list = list()
        for post in post_list:
            data = {
                "id": post.pk,
                "title": post.title,
                "genre": post.genre,
                "instrument": post.instrument,
                "num_liked": post.num_liked,
                "num_comments": post.num_comments,
                "created_date": post.created_date,
            }
            data_list.append(data)
        return data_list


# 유저 모델 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    post_set = PostListField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    followers = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    liked_posts = PostListField(read_only=True)
    profile_img = serializers.ImageField(read_only=True, use_url=False)
    profile_bg = serializers.ImageField(read_only=True, use_url=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nickname',
            'profile_img',
            'profile_bg',
            'instrument',
            'user_type',
            'genre',
            'total_liked',
            'liked_posts',
            'num_followings',
            'following',
            'num_followers',
            'followers',
            'is_active',
            'last_login',
            'post_set',
        )
        read_only_fields = (
            'email',
            'user_type',
            'profile_img',
            'profile_bg',
            'total_liked',
            'is_active',
            'last_login',
            'post_set',
        )


class ProfileImageField(serializers.ImageField):
    queryset = User.objects.all()

    def to_representation(self, value):
        if not value:
            return None
        p = re.compile(r'(user_\d+/profile_img/)')
        path = p.match(value.name).group(1)

        data = {
            "original_img": value.name,
            "profile_img_200": f"{path}profile_img_200.png",
            "profile_img_400": f"{path}profile_img_400.png",
        }
        return data


class ProfileBackgroundField(serializers.ImageField):
    queryset = User.objects.all()

    def to_representation(self, value):
        if not value:
            return None
        p = re.compile(r'(user_\d+/profile_bg/)')
        path = p.match(value.name).group(1)

        data = {
            "original_img": value.name,
            "profile_bg": f"{path}profile_bg.png",
        }
        return data


class ProfileImageSerializer(serializers.ModelSerializer):
    profile_img = ProfileImageField()
    profile_bg = ProfileBackgroundField()

    class Meta:
        model = User
        fields = (
            'profile_img',
            'profile_bg'
        )


# 회원가입 시리얼라이저
class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nickname',
            'genre',
            'instrument',
            'password1',
            'password2',
        )

    # 악기를 여러개 받을 수 있어야 한다
    # 여러 체크박스를 통해 'instrument' 이름으로 여러 값이 올때, list 형태로 온다는 것을 이용한다
    # instrument list 를 ','로 구분된 문자열로 변환한다
    # def validate_instrument(self, data):
    #     data['instrument'] = ','.join(data['instrument'])
    #     return data

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return data

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data.get('email'),
            nickname=validated_data.get('nickname'),
            password=validated_data.get('password1'),
            genre=validated_data.get('genre'),
            instrument=validated_data.get('instrument'),
        )
