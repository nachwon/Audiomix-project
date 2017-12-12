from datetime import datetime
from django.utils import timezone

from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

# from config_secret import settings as secret_settings
from utils.permissions import IsOwnerOrReadOnly
from utils.tasks.mail import (
    send_verification_mail,
    send_confirm_readmission_mail,
    send_verification_mail_after_social_login,
)
from utils.encryption import encrypt, decrypt
from .models import ActivationKeyInfo, Relationship
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
    def get(self, request):
        """
        1. 소셜로그인으로 생성된 유저가, Soundhub Signup 을 시도하는 경우 Signup.post() 함수에서 인증메일을 보내준다
        2. 인증 메일에는 Signup view 에 get 요청을 보내는 링크를 포함한다
        3. get parameter 로 전달된 정보를 사용해서
        4. 어떤 방식으로도 로그인할 수 있도록 Soundhub password 추가

        :param request:
            GET = {
                'activation_key': Encrypted Activation Key,
                'nickname': 사용자 입력 닉네임,
                'password': Encrypted Password,
                'instrument': 사용자 입력 악기정보,
            }
        :return: None
        """
        # get parameter 에서 값 추출
        # 암호화된 activation key 와
        activation_key = decrypt(
            key=secret_settings.ENCRYPTION_KEY,
            encrypted_text=request.GET['activation_key'],
        )
        password = decrypt(
            key=secret_settings.ENCRYPTION_KEY,
            encrypted_text=request.GET['password'],
        )
        nickname = request.GET['nickname']
        instrument = request.GET['instrument']

        # activation key 에 해당하는 유저가 존재하는지 검사
        activation_key_info = get_object_or_404(ActivationKeyInfo, key=activation_key)
        # activation key 가 만료된 경우
        if not activation_key_info.expires_at > timezone.now():
            raise APIException('activation_key 의 기한이 만료되었습니다.')

        # 해당 유저 정보를 변경하고 저장
        user = activation_key_info.user
        user.nickname = nickname
        user.set_password(password)
        user.instrument = instrument
        user.save()

        data = {
            'token': user.token,
            'user': UserSerializer(user).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        1. 전달된 email 의 유저가 존재하는 경우
            1) 소셜로그인 계정일 때
                - 추가 회원가입 링크를 담은 인증 메일 발송
            2) Soundhub 계정일 때
                a. is_active 가 True
                    - APIException: '이미 존재하는 유저입니다'
                b. is_active 가 False
                    - 안내 메일 발송
                    - APIException: '이메일 인증 중인 유저입니다. 메일을 확인해주세요.'

        2. 전달된 email 의 유저가 존재하지 않는 경우
            - User, ActivationKeyInfo 생성
            - 인증메일 발송

        :param request:
            data = {
                'email': 'useremail@example.com',
                'nickname': 'user_nickname',
                'password1': 'password',
                'password2': 'password',
                'instrument': 'instrument_name'
            }

        :return:
            유저 생성 성공: User serializer 데이터 (HTTP status 201)
            유저 생성 실패: User serializer 의 error 정보 (HTTP status 400)
        """
        # 유저 타입 상수
        soundhub = User.USER_TYPE_SOUNDHUB

        email = request.data['email']
        # 전달된 이메일의 유저가 존재하는 경우
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # 소셜로그인 계정인 경우
            if not user.user_type == soundhub:
                # password 암호화
                encrypted_password = encrypt(
                    key=secret_settings.ENCRYPTION_KEY,
                    plain_text=request.data['password'],
                )
                # 유저의 activation key 새로 설정
                user.activationkeyinfo.refresh()
                # activation key info 암호화
                encrypted_activation_key = encrypt(
                    key=secret_settings.ENCRYPTION_KEY,
                    plain_text=user.activationkeyinfo.key,
                )
                data = {
                    'activation_key': encrypted_activation_key,
                    'nickname': request.data['nickname'],
                    'password': encrypted_password,  # password 암호화
                    'instrument': request.data['instrument'],
                }
                # 유저 정보를 담은 데이터와 함께 메일 발송
                send_verification_mail_after_social_login.delay(data, [user.email])
            # Soundhub 계정일 때
            elif user.is_active is True:
                raise APIException('이미 존재하는 유저입니다')
            elif user.is_active is False:
                send_confirm_readmission_mail.delay([user.email])
                raise APIException('이메일 인증 중인 유저입니다. 메일을 확인해주세요.')

        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            # user 생성, 반환
            user = serializer.save()
            # activation key 생성
            activation_key_info = ActivationKeyInfo.objects.create(user=user)
            # 인증 메일 발송
            send_verification_mail.delay(
                activation_key=activation_key_info.key,
                recipient_list=[user.email],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(APIView):
    @staticmethod
    def post(request):
        """
        request 에는 token 과 client_id 값이 와야 한다
        token 의 경우, scope 에 'profile'과 'email'을 포함해 발급받은 토큰이어야 한다.

        id_info = {
            // These six fields are included in all Google ID Tokens.
            "iss": "https://accounts.google.com",
            "sub": "110169484474386276334",
            "azp": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
            "aud": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
            "iat": "1433978353",
            "exp": "1433981953",

            // These seven fields are only included when the user has granted the "profile" and
            // "email" OAuth scopes to the application.
            "email": "testuser@gmail.com",
            "email_verified": "true",
            "name" : "Test User",
            "picture": "https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg",
            "given_name": "Test",
            "family_name": "User",
            "locale": "en"
        }
        :param request:
        :return:
        """
        token = request.data['token']
        client_id = request.data['client_id']
        nickname = request.data['nickname']
        instrument = request.data['instrument']

        try:
            # token 을 인증하고, 토큰 내부 정보를 가져옴
            id_info = id_token.verify_oauth2_token(token, requests.Request(), client_id)
            # token 발행정보 확인
            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
        except ValueError:
            raise APIException('token 또는 client_id 가 유효하지 않습니다')

        # 이미 존재하는 유저일 경우 유저 생성 없이 기존 유저 반환
        if User.objects.filter(email=id_info['email']).exists():
            user = User.objects.get(email=id_info['email'])
            user.is_active = True
            user.save()
        # 닉네임이 존재할 경우
        elif User.objects.filter(nickname=nickname).exists():
            raise APIException('이미 존재하는 닉네임입니다')
        else:
            # 토큰 정보로 유저 생성. 이메일 인증 생략하고 바로 is_active=True
            user = User(
                email=id_info['email'],
                nickname=nickname,
                instrument=instrument,
                user_type=User.USER_TYPE_GOOGLE,
                is_active=True,
                last_login=datetime.now(),
            )
            user.save()

        data = {
            'token': user.token,
            'user': UserSerializer(user).data,
            # 'is_active': user.is_active,  # 디버그용
        }
        return Response(data, status=status.HTTP_201_CREATED)


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
        saved_activation_key_info = ActivationKeyInfo.objects.get(key=activation_key)

        data = {
            'user': UserSerializer(activation_key_info.user).data,
            'is_active': saved_activation_key_info.user.is_active,
        }
        return Response(data, status=status.HTTP_200_OK)


class FollowUserToggle(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def post(self, request, *args, **kwargs):
        to_user_instance = self.get_object()
        from_user_instance = request.user

        if to_user_instance in from_user_instance.following.all():
            relation = Relationship.objects.get(to_user_id=to_user_instance.pk,
                                                from_user_id=from_user_instance.pk)
            relation.delete()
        else:
            Relationship.objects.create(to_user_id=to_user_instance.pk,
                                        from_user_id=from_user_instance.pk)

        from_user_instance.save_num_relations()
        to_user_instance.save_num_relations()

        data = UserSerializer(from_user_instance).data
        return Response(data)
