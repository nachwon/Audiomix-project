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


# 프로필 이미지를 위한 커스텀 필드
class ProfileImageField(serializers.ImageField):
    # 객체 저장을 위한 queryset 지정
    queryset = User.objects.all()

    # 보여줄 때
    def to_representation(self, value):
        # value 는 DefaultStaticImageFieldFile 객체
        # 상대경로를 보여주기 위한 정규표현식
        pattern = re.compile(r'.*/che1-soundhub/(.*)[?]')
        # value.url 을 호출하여 파일이 있으면 파일의 절대경로를 가져오고
        # 없으면 디폴트 이미지의 절대경로를 가져옴
        # 받은 절대경로를 잘라서 상대경로로 바꿔준 뒤 리턴
        result = pattern.match(value.url).group(1)
        return result

    # 저장할 때
    def to_internal_value(self, data):
        # 받은 data(파일 객체) 그대로 넘겨줌
        return data


# 유저 모델 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    post_set = PostListField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    followers = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    liked_posts = PostListField(read_only=True)
    # 커스팀 필드 ProfileImageField 를 사용해서 profile_img 필드 처리
    profile_img = ProfileImageField()

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
            'total_liked',
            'is_active',
            'last_login',
            'post_set',
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
