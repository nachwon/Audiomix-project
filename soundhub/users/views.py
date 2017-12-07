import hashlib
from datetime import datetime, timedelta
from django.utils import timezone
from random import random

from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.mail import send_verification_mail
from utils.permissions import IsOwnerOrReadOnly
from .models import ActivationKeyInfo
from .serializers import UserSerializer, SignupSerializer

User = get_user_model()


# 사용자 본인 계정 조회, 수정, 삭제
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        # 커스텀 권한
        IsOwnerOrReadOnly,
    )


# 유저 목록 조회
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )


# 로그인
class Login(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(email=email, password=password)
        if user:
            token, is_token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': 'Invalid credentials'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


# 회원가입
class Signup(APIView):
    def post(self, request):
        """
        :param request:
            request.data = {
                'email': 'useremail@example.com',
                'nickname': 'user_nickname',
                'password1': 'password',
                'password2': 'password',
                'instrument': 'instrument_name'
            }

        :process:
            User 생성,
            ActivationKeyInfo 생성,
            인증 메일 발송

        :return:
            유저 생성 성공: User serializer 데이터 (HTTP status 201)
            유저 생성 실패: User serializer 의 error 정보 (HTTP status 400)
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            # 방금 생성한 user
            user = serializer.save()
            """
            이메일 인증 활성화 하려면 아래의 코드 Uncomment
            """
            # activation key 생성을 위한 무작위 문자열
            # user 마다 unique 한 값을 가지게 하기 위해 user.email 첨가
            # random_string = str(random()) + user.email
            # # sha1 함수로 영문소문자 또는 숫자로 이루어진 40자의 해쉬토큰 생성
            # activation_key = hashlib.sha1(random_string.encode('utf-8')).hexdigest()
            # # activation key 유효기간 2일
            # expires_at = datetime.now() + timedelta(days=2)
            # # activation key 생성
            # ActivationKeyInfo.objects.create(
            #     user=user,
            #     key=activation_key,
            #     expires_at=expires_at,
            # )
            # # 인증 메일 발송
            # send_verification_mail(
            #     activation_key=activation_key,
            #     recipient_list=[user.email],
            # )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUser(APIView):
    def get(self, request):
        """
        activation_key 받고, key 정보가 일치하는 유저의 is_active = True

        :param request: activation_key 정보가 들어옴
        :return: user 정보와 is_active
        """
        activation_key = request.GET['activation_key']
        # activation key 와 일치하는 정보가 없으면 HTTP status 404
        activation_key_info = get_object_or_404(ActivationKeyInfo, key=activation_key)
        # activation key 가 만료된 경우
        if not activation_key_info.expires_at > timezone.now():
            raise APIException('activation_key 의 기한이 만료되었습니다.')
        # activation key 와 일치하는 정보가 있고, key 가 유효할 경우
        activation_key_info.user.is_active = True
        # user.save()
        activation_key_info.user.save()
        data = UserSerializer(activation_key_info.user).data
        return Response(data)
