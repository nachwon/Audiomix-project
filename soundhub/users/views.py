from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer, SignupSerializer

from utils.permissions import IsOwnerOrReadOnly

User = get_user_model()


# 사용자 본인 계정 조회, 수정, 삭제
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        # 커스텀 권한
        IsOwnerOrReadOnly,
    )


# 사용자 계정 생성
class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer


class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                serializer = UserSerializer(user)
                data = {
                    "user": serializer.data,
                }
            else:
                data = {"error": "login failed"}
            return Response(data, status=status.HTTP_200_OK)
