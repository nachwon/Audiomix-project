from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


# 회원 가입시 이메일, 악기, 비밀번호를 받도록 하는 커스텀 매니저 설정
class CustomUserManager(BaseUserManager):
    # 일반유저 생성 - create_user 메서드 오버라이드
    def create_user(self, email, instrument, password):
        # 이메일을 입력하지 않은 경우 에러 발생
        if not email:
            raise ValueError('이메일을 반드시 입력해야 합니다.')

        # 입력받은 email, instrument 값으로 유저 인스턴스를 생성
        user = self.model(
            email=self.normalize_email(email),  # 이메일 주소를 소문자화하여 노멀라이즈
            instrument=instrument,
        )

        # 유저 인스턴스에 비밀번호 설정
        user.set_password(password)

        # 생성된 유저 인스턴스를 DB에 저장
        user.save()

        # 생성된 유저 리턴
        return user

    # 관리자 유저 생성 - create_superuser 매서드 오버라이드
    def create_superuser(self, email, password, instrument=None):
        # 유저 인스턴스 생성
        user = self.model(
            email,
            instrument,
            password,
        )
        # 관리자 여부 값 설정
        user.is_admin = True

        # 유저 저장
        user.save()
        return user


# 이메일을 아이디로 사용하는 커스텀 유저 모델
class CustomUser(AbstractBaseUser):
    # 이메일 주소
    email = models.EmailField(
        verbose_name='이메일 주소',
        max_length=255,
        unique=True,
    )

    # 악기 선택지
    INSTRUMENT_CHOICES = (
        ('G', 'Guitar'),
        ('B', 'Base'),
        ('D', 'Drums'),
        ('V', 'Vocals'),
        ('K', 'Keyboard'),
        ('O', 'Others'),
    )
    # 사용 악기
    instrument = models.CharField(max_length=1, choices=INSTRUMENT_CHOICES)

    # 관리자 여부
    is_admin = models.BooleanField(default=False)

    # 이메일을 유저네임으로 설정
    USERNAME_FIELD = 'email'

    # 필수 정보 설정
    REQUIRED_FIELDS = (
        'email',
        'instrument',
    )

    # 커스텀 유저 매니저를 사용하도록 설정
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin




