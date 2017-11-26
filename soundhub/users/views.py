from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions

from users.models import User
from users.serializers import UserSerializer


# 사용자 프로필 확인
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
