from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.fields import PostSetField, LikedPostsField, ProfileImageField, BypassEmptyStringField

User = get_user_model()


# 유저 모델 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    post_set = PostSetField(read_only=True)
    liked_posts = LikedPostsField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    followers = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
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


class ProfileImageSerializer(serializers.ModelSerializer):
    profile_img = ProfileImageField()
    profile_bg = BypassEmptyStringField(use_url=False)

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

    # 비밀번호 일치 검사
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
