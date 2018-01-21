from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, generics, filters
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import ENCRYPTION_KEY
from users.exceptions import (
    RequestDataDoesNotExist,
    UniqueFieldDuplication,
    RequestDataInvalid,
)
from utils.permissions import IsOwnerOrReadOnly
from utils.rescale_img import make_profile_img, make_profile_bg
from utils.tasks.mail import (
    send_verification_mail,
    send_confirm_readmission_mail,
    send_verification_mail_after_social_login,
    send_password_reset_mail,
)
from utils.encryption import encrypt, decrypt
from .models import ActivationKeyInfo, Relationship
from .serializers import UserSerializer, SignupSerializer, ProfileImageSerializer

User = get_user_model()


# 사용자 본인 계정 조회, 수정, 삭제
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        # 커스텀 권한
        IsOwnerOrReadOnly,
    )


class ProfileImage(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileImageSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )

    # 패치 요청을 받았을 때
    # request.data 에 profile_img 가 있으면
    # 이미지 관련 작업 실행
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        profile_img = request.data.get('profile_img', False)
        profile_bg = request.data.get('profile_bg', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if profile_img:
            make_profile_img(instance, profile_img)
        elif profile_img == '':
            instance.profile_img.delete()

        if profile_bg:
            make_profile_bg(instance, profile_bg)
        elif profile_bg == '':
            instance.profile_bg.delete()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# 유저 목록 조회
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    # filter_fields = (
    #     'instrument',
    #     'genre',
    # )
    ordering_fields = (
        'total_liked',
        'num_followers',
    )


class Login(APIView):
    def post(self, request):
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


class Logout(APIView):
    def post(self, request):
        if request.user is not AnonymousUser:
            token = get_object_or_404(Token, user=request.user)
            token.delete()
            data = {
                "detail": "로그아웃 되었습니다."
            }
            return Response(data, status=status.HTTP_200_OK)


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
        # 암호화된 activation key 와 password 복호화
        activation_key = decrypt(
            key=ENCRYPTION_KEY,
            encrypted_text=request.GET['activation_key'],
        )
        password = decrypt(
            key=ENCRYPTION_KEY,
            encrypted_text=request.GET['password'],
        )
        nickname = request.GET['nickname']
        instrument = request.GET['instrument']

        # activation key 에 해당하는 유저가 존재하는지 검사
        activation_key_info = get_object_or_404(ActivationKeyInfo, key=activation_key)
        # activation key 가 만료된 경우
        if not activation_key_info.expires_at > timezone.now():
            raise RequestDataInvalid('activation_key 의 기한이 만료되었습니다.')

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
                    - RequestDataInvalid: '이미 존재하는 유저입니다'
                b. is_active 가 False
                    - 안내 메일 발송
                    - RequestDataInvalid: '이메일 인증 중인 유저입니다. 메일을 확인해주세요.'

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
                    key=ENCRYPTION_KEY,
                    plain_text=request.data['password'],
                )
                # 유저의 activation key 새로 설정
                user.activationkeyinfo.refresh()
                # activation key info 암호화
                encrypted_activation_key = encrypt(
                    key=ENCRYPTION_KEY,
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
                raise RequestDataInvalid('이미 존재하는 유저입니다')
            elif user.is_active is False:
                send_confirm_readmission_mail.delay([user.email])
                raise RequestDataInvalid('이메일 인증 중인 유저입니다. 메일을 확인해주세요.')

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
            data = {
                'token': Google token,
                'client_id': Google Client ID,
            }
        :return: Response(user 객체, token)
        """
        # Request Data 검사
        if 'token' not in request.data:
            raise RequestDataDoesNotExist('토큰이 없습니다')
        if 'client_id' not in request.data:
            raise RequestDataDoesNotExist('Google Client ID 가 없습니다')

        token = request.data['token']
        client_id = request.data['client_id']

        try:
            # token 을 인증하고, 토큰 내부 정보를 가져옴
            id_info = id_token.verify_oauth2_token(token, google_requests.Request(), client_id)
            # token 발행정보 확인
            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise RequestDataInvalid('토큰이 유효하지 않습니다')
        except RequestDataInvalid:
            raise RequestDataInvalid('token 또는 client_id 가 유효하지 않습니다')

        # 이미 존재하는 유저일 경우 유저 생성 없이 기존 유저 반환
        if User.objects.filter(email=id_info['email']).exists():
            user = User.objects.get(email=id_info['email'])
            user.is_active = True
            user.save()
            data = {
                'token': user.token,
                'user': UserSerializer(user).data,
                # 'is_active': user.is_active,  # 디버그용
            }
            return Response(data, status=status.HTTP_200_OK)

        # 존재하지 않는 유저일 경우만 받음
        if 'nickname' not in request.data:
            raise RequestDataDoesNotExist('nickname 이 없습니다')
        nickname = request.data['nickname']
        instrument = request.data['instrument'] if 'instrument' in request.data else None

        # 닉네임이 존재할 경우
        if User.objects.filter(nickname=nickname).exists():
            raise UniqueFieldDuplication('이미 존재하는 닉네임입니다')
        else:
            # 토큰 정보로 유저 생성. 이메일 인증 생략하고 바로 is_active=True
            user = User(
                email=id_info['email'],
                nickname=nickname,
                instrument=instrument,
                user_type=User.USER_TYPE_GOOGLE,
                is_active=True,
                last_login=timezone.now(),
            )
            user.save()

        data = {
            'token': user.token,
            'user': UserSerializer(user).data,
            # 'is_active': user.is_active,  # 디버그용
        }
        return Response(data, status=status.HTTP_201_CREATED)


class FacebookLogin(APIView):
    def post(self, request):
        """
        Facebook token, facebook_user_id 를 받아서 유효성 검사 후
        해당 토큰으로 생성된 유저가 있으면 반환, 없으면 생성

        :param request:
            data = {
                'access_token': facebook token,
                'facebook_user_id': facebook user id,
            }
        :return: Response(user 객체, token)
        """

        # token 값의 유효성을 검사하기 위한 정보를 저장하는 클래스
        class DebugTokenInfo(NamedTuple):
            app_id: str
            application: str
            expires_at: int
            is_valid: bool
            issued_at: int
            scopes: list
            type: str
            user_id: str

        # 받아온 토큰 값이 진짜 토큰인지 확인하는 메서드
        def get_debug_token_info(access_token):
            app_id = settings.FACEBOOK_APP_ID
            app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
            app_access_token = f'{app_id}|{app_secret_code}'

            params = {
                'input_token': access_token,
                'access_token': app_access_token,
            }
            response = requests.get('https://graph.facebook.com/debug_token', params=params)
            if 'error' in response.json()['data']:
                raise RequestDataInvalid('잘못된 토큰입니다')
            return DebugTokenInfo(**response.json()['data'])

        # Request Data 검사
        if 'access_token' not in request.data:
            raise RequestDataDoesNotExist('토큰이 없습니다')
        if 'facebook_user_id' not in request.data:
            raise RequestDataDoesNotExist('Facebook User ID 가 없습니다')

        # 토큰 유효성 검사
        debug_token_info = get_debug_token_info(request.data['access_token'])
        if debug_token_info.user_id != request.data['facebook_user_id']:
            raise RequestDataInvalid('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')
        if not debug_token_info.is_valid:
            raise RequestDataInvalid('페이스북 토큰이 유효하지 않음')

        # FacebookBackend 를 사용해서 유저 인증
        user = authenticate(facebook_user_id=request.data['facebook_user_id'])
        # 해당 토큰으로 생성된 유저가 존재하는 경우, 해당 유저 반환
        if user:
            user.is_active = True
            user.save()
            data = {
                'token': user.token,
                'user': UserSerializer(user).data,
                # 'is_active': user.is_active,  # 디버그용
            }
            return Response(data, status=status.HTTP_200_OK)
        # 해당 토큰으로 생성된 유저가 없는 경우, 새 유저 생성
        else:
            try:
                email = request.data['email']
                nickname = request.data['nickname']
                instrument = request.data['instrument'] if 'instrument' in request.data else None
            except RequestDataDoesNotExist:
                raise RequestDataDoesNotExist('유저를 생성할 데이터가 없습니다')

            # 이메일 또는 닉네임이 존재할 경우
            if User.objects.filter(email=email).exists():
                raise UniqueFieldDuplication('이미 존재하는 이메일입니다')
            if User.objects.filter(nickname=nickname).exists():
                raise UniqueFieldDuplication('이미 존재하는 닉네임입니다')

            # 인증에 실패한 경우 페이스북유저 타입으로 유저를 만들어줌
            user = User.objects.create_user(
                email=email,
                nickname=nickname,
                instrument=instrument,
                is_active=True,
                user_type=User.USER_TYPE_FACEBOOK,
            )
            # 유저 시리얼라이즈 결과를 Response
            data = {
                'user': UserSerializer(user).data,
                'token': user.token,
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
            raise RequestDataInvalid('activation_key 의 기한이 만료되었습니다.')
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

    def post(self, request):
        to_user_instance = self.get_object()
        from_user_instance = request.user

        if to_user_instance in from_user_instance.following.all():
            relation = Relationship.objects.get(
                to_user_id=to_user_instance.pk,
                from_user_id=from_user_instance.pk
            )
            relation.delete()
        else:
            Relationship.objects.create(
                to_user_id=to_user_instance.pk,
                from_user_id=from_user_instance.pk
            )

        from_user_instance.save_num_relations()
        to_user_instance.save_num_relations()

        data = UserSerializer(from_user_instance).data
        return Response(data)


class ResetPassword(APIView):
    def get(self, request):
        """
        password 변경 링크를 통해서만 접근 가능
        activation key 로 유효한 접근인지 확인 후
        get parameter 로 전달된 정보로 password 재설정

        :param request: 암호화된 activation key 와 password 정보
        :return: Response(1)
        """
        try:
            # get parameter 에서 값 추출
            # 암호화된 activation key 와 password 복호화
            activation_key = decrypt(
                key=ENCRYPTION_KEY,
                encrypted_text=request.GET['activation_key'],
            )
            password = decrypt(
                key=ENCRYPTION_KEY,
                encrypted_text=request.GET['password'],
            )
        except RequestDataDoesNotExist:
            raise RequestDataDoesNotExist('잘못된 요청입니다')

        # activation key 에 해당하는 유저가 존재하는지 검사
        activation_key_info = get_object_or_404(ActivationKeyInfo, key=activation_key)
        # activation key 가 만료된 경우
        if not activation_key_info.expires_at > timezone.now():
            raise RequestDataInvalid('activation_key 의 기한이 만료되었습니다.')

        # password 변경
        activation_key_info.user.set_password(password)
        activation_key_info.user.save()

        return Response(1, status=status.HTTP_200_OK)

    def post(self, request):
        """
        password 를 변경하기 전, 유저 본인이 맞는지 확인하기 위해 password 재검사

        :param request: password
        :return: Response(1)
        """
        if 'password' not in request.data:
            raise RequestDataDoesNotExist('password 값이 없습니다')
        password = request.data['password']

        # password 가 맞는지 검사
        if not request.user.check_password(password):
            raise RequestDataInvalid('password 가 유효하지 않습니다')

        return Response(1, status=status.HTTP_200_OK)

    def put(self, request):
        """
        비밀번호 변경 메일 발송

        :param request:
            data = {
                'password1': 비밀번호
                'password2': 확인용 비밀번호
            }
        :return: Response(1)
        """
        try:
            password1 = request.data['password1']
            password2 = request.data['password2']
        except RequestDataDoesNotExist:
            raise RequestDataDoesNotExist('password1 또는 password2 값이 전달되지 않았습니다')

        if password1 == password2:
            # password 암호화
            encrypted_password = encrypt(
                key=ENCRYPTION_KEY,
                plain_text=request.data['password1'],
            )
            # 유저의 activation key 새로 설정
            request.user.activationkeyinfo.refresh()
            # activation key info 암호화
            encrypted_activation_key = encrypt(
                key=ENCRYPTION_KEY,
                plain_text=request.user.activationkeyinfo.key,
            )

            data = {
                'activation_key': encrypted_activation_key,
                'password': encrypted_password,  # password 암호화
            }
            # password 변경 메일 발송
            send_password_reset_mail.delay(data, [request.user.email])

            return Response(1, status=status.HTTP_200_OK)

        else:
            raise RequestDataInvalid('password1 과 password2 가 일치하지 않습니다')
