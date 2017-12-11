from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# 유저 모델 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nickname',
            'instrument',
            'user_type',
            'is_staff',
            'last_login',
            'created_at',
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
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password1'],
            instrument=validated_data['instrument'],
        )


# class ActivationKeyInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ActivationKeyInfo
#         fields = ('user', 'key', 'expires_at')
#
#     # def validate(self, data):
#     #     if len(data['key']) < 40:
#     #         raise serializers.ValidationError('올바른 key 값이 아닙니다.')
#     #     return data
