from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# 회원 가입시 이메일, 닉네임, 악기, 비밀번호를 받도록 하는 커스텀 매니저 설정
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    # 유저 생성 공통 메서드
    def _create_user(self, email, nickname, password, is_staff, is_active, instrument=None):
        # 이메일을 입력하지 않은 경우 에러 발생
        if not email:
            raise ValueError('이메일을 반드시 입력해야 합니다.')

        # 입력받은 email, nickname, instrument 값으로 유저 인스턴스를 생성
        user = self.model(
            email=self.normalize_email(email),  # 이메일 주소를 소문자화하여 노멀라이즈
            nickname=nickname,
            is_staff=is_staff,
            is_active=is_active,
            instrument=instrument,
        )

        # 유저 인스턴스에 비밀번호 설정
        user.set_password(password)

        # 생성된 유저 인스턴스를 DB에 저장
        user.save()

        # 생성된 유저 리턴
        return user

    # 관리자 유저 생성 - create_superuser 매서드 오버라이드
    def create_superuser(self, email, nickname, password, instrument=None):
        # _create_user 메서드를 사용하고 is_staff 값을 True로 설정
        user = self._create_user(
            email=email,
            nickname=nickname,
            password=password,
            is_staff=True,
            is_active=True,
            instrument=instrument,
        )
        return user

    # 일반 유저 생성 - create_user 메서드 오버라이드
    def create_user(self, email, nickname, password, instrument=None):
        # _create_user 메서드를 사용하고 is_staff 값을 False로 설정
        user = self._create_user(
            email=email,
            nickname=nickname,
            password=password,
            is_staff=False,
            # 이메일 인증 사용시 False
            is_active=True,
            instrument=instrument,
        )
        return user


# 이메일을 아이디로 사용하는 커스텀 유저 모델
# PermissionsMixin 을 상속받아서 권한 관련 메서드들을 포함
class User(AbstractBaseUser, PermissionsMixin):
    # 이메일 주소
    email = models.EmailField(
        verbose_name='이메일 주소',
        max_length=255,
        unique=True,
    )
    # 닉네임
    nickname = models.CharField(max_length=50, unique=True)

    # Guitar, Base, Drum, Vocal, Keyboard, Other 등은 프론트에서 체크박스 value 로 받고,
    # Serializer 에서 문자열로 합쳐줌
    instrument = models.CharField(max_length=255, blank=True, null=True)

    # 총 좋아요 수
    total_liked = models.IntegerField(default=0)

    # 관리자 여부
    is_staff = models.BooleanField()
    # 활성화 여부
    is_active = models.BooleanField()
    # 계정생성 날짜
    created_at = models.DateField(auto_now_add=True)

    # 이메일을 유저네임으로 설정
    USERNAME_FIELD = 'email'

    # 필수 정보 설정
    REQUIRED_FIELDS = (
        'nickname',
    )

    # 커스텀 유저 매니저를 사용하도록 설정
    objects = CustomUserManager()

    def __str__(self):
        return self.nickname

    # 유저의 모든 포스트들이 받은 좋아요 갯수를 총합하여 total_liked 필드에 저장
    def save_total_liked(self, *args, **kwargs):
        posts = self.post_set.all()
        total_liked = sum([i.num_liked for i in posts])
        self.total_liked = total_liked
        self.save(*args, **kwargs)

    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0].key

    # 필수 메서드들
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        return True


# Email Verification 에 사용되는 Activation key 정보를 담고 있는 클래스
# User class 와 one to one 으로 연결
class ActivationKeyInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, blank=True)
    # key 만료 기한
    expires_at = models.DateTimeField()
