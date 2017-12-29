import hashlib
from datetime import datetime, timedelta
from random import random

from django.contrib.auth import get_user_model

from users.models import ActivationKeyInfo

User = get_user_model()


# Test Code 작성시 필요한 dummy user 를 생성하는 클래스
class DummyUser:
    # 인스턴스 생성시 unique 한 필드를 생성하기 위해 'unique'를 받음
    def __init__(self, unique=''):
        self.EMAIL = f'dummy{unique}@gmail.com'
        self.PASSWORD = 'password'
        self.NICKNAME = f'dummy{unique}'
        self.INSTRUMENT = 'instrument'

    def create(self):
        return User.objects.create_user(
            email=self.EMAIL,
            nickname=self.NICKNAME,
            password=self.PASSWORD,
            instrument=self.INSTRUMENT,
        )

    def create_superuser(self):
        return User.objects.create_superuser(
            email=self.EMAIL,
            nickname=self.NICKNAME,
            password=self.PASSWORD,
            instrument=self.INSTRUMENT,
        )

    # 유저 대량 생산
    @staticmethod
    def create_massive(num):
        user_list = list()
        for i in range(num):
            user = DummyUser(str(i)).create()
            user_list.append(user)
        return user_list


# Test Code 작성시 필요한 dummy activation key info 를 생성하는 클래스
class DummyActivationKeyInfo:
    def __init__(self, unique='', user=None):
        self.dummy_user = DummyUser(unique)
        self.user = self.dummy_user.create() if not user else user

    def create(self):
        return ActivationKeyInfo.objects.create(
            user=self.user,
        )

    # dummy activation key info 대량 생산
    @staticmethod
    def create_massive(num):
        aki_list = list()
        for i in range(num):
            aki = DummyActivationKeyInfo(str(i)).create()
            aki_list.append(aki)
        return aki_list

