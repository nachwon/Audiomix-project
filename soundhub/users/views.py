from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions

from users.models import User
from users.serializers import UserSerializer, SignupSerializer


# 사용자 본인 계정 조회, 수정, 삭제
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )


# 사용자 계정 생성
class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
