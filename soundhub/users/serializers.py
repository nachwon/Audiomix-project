from rest_framework import serializers

from users.models import User


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
            'is_superuser',
            'last_login',
        )
