import hashlib
from datetime import datetime, timedelta
from random import random

from django.contrib.auth import get_user_model

from users.models import ActivationKeyInfo

User = get_user_model()


class DummyUser:
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


class DummyActivationKeyInfo:
    def __init__(self, unique='', user=None, activation_key=None, expires_at=None):
        self.dummy_user = DummyUser(unique)
        self.user = self.dummy_user.create() if not user else user

    def create(self):
        return ActivationKeyInfo.objects.create(
            user=self.user,
        )
