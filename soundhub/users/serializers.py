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
            'is_staff',
            'last_login',
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

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            instrument=validated_data['instrument'],
        )
        user.set_password(validated_data['password1'],)
        user.save()
        return user
