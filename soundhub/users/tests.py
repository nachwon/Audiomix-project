import hashlib
from datetime import datetime, timedelta
from random import random

from django.contrib.auth import get_user_model, authenticate
from django.core import mail
from django.test import TestCase, TransactionTestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer

from users.dummy import DummyUser, DummyActivationKeyInfo
from users.models import ActivationKeyInfo
from users.serializers import UserSerializer
from utils.mail import send_verification_mail

User = get_user_model()


class UserModelTest(TransactionTestCase):
    DUMMY_EMAIL = 'dummy1@gmail.com'
    DUMMY_PASSWORD = 'password'
    DUMMY_NICKNAME = 'dummy1'
    DUMMY_INSTRUMENT = 'instrument'

    REQUIRED_FIELDS = (
        'nickname',
        'instrument',
    )

    def test_fields_with_default_value(self):
        """
        user 를 기본값으로 설정했을 때 default 값이 잘 들어 있나
        :return:
        """
        user = User.objects.create_user(
            email=self.DUMMY_EMAIL,
            nickname=self.DUMMY_NICKNAME,
            password=self.DUMMY_PASSWORD,
            instrument=self.DUMMY_INSTRUMENT,
        )

        # 기본 필드 검사
        self.assertEqual(user.email, self.DUMMY_EMAIL)
        self.assertEqual(user.nickname, self.DUMMY_NICKNAME)
        self.assertEqual(user.check_password(self.DUMMY_PASSWORD), True)
        self.assertEqual(user.instrument, self.DUMMY_INSTRUMENT)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, False)
        self.assertIsNotNone(user.created_at)

        self.assertEqual(user.USERNAME_FIELD, 'email')
        self.assertEqual(user.REQUIRED_FIELDS, self.REQUIRED_FIELDS)

        # is_active = True 주고 인증 잘 되는지 검사
        user.is_active = True
        user.save()
        self.assertEqual(user, authenticate(
            email=self.DUMMY_EMAIL,
            password=self.DUMMY_PASSWORD,
        ))


class ActivationKeyInfoModelTest(TransactionTestCase):
    DUMMY_EMAIL = 'dummy-@gmail.com'
    DUMMY_PASSWORD = 'password'
    DUMMY_NICKNAME = 'dummy-'
    DUMMY_INSTRUMENT = 'instrument'

    def test_activation_key_info_with_default_value(self):
        dummy_user = DummyUser()
        user = dummy_user.create()

        # user = User.objects.create_user(
        #     email=self.DUMMY_EMAIL,
        #     nickname=self.DUMMY_NICKNAME,
        #     password=self.DUMMY_PASSWORD,
        #     instrument=self.DUMMY_INSTRUMENT,
        # )
        random_string = str(random()) + user.email
        activation_key = hashlib.sha1(random_string.encode('utf-8')).hexdigest()
        expires_at = datetime.now() + timedelta(days=2)

        activation_key_info = ActivationKeyInfo.objects.create(
            user=user,
            key=activation_key,
            expires_at=expires_at,
        )

        # 기본 필드 검사
        self.assertEqual(activation_key_info.user, user)
        self.assertEqual(activation_key_info.key, activation_key)
        self.assertEqual(activation_key_info.expires_at, expires_at)

        # user 와 잘 연결이 되어있는가
        self.assertEqual(user.activationkeyinfo, activation_key_info)

        # user 가 삭제되면 activation_key_info 도 같이 삭제되는가
        len_before = len(ActivationKeyInfo.objects.all())
        user.delete()
        len_after = len(ActivationKeyInfo.objects.all())
        self.assertEqual(len_before, len_after+1)


class SendVerificationMailTest(TestCase):
    def test_send_verification_mail(self):
        dummy_activation_key_info = DummyActivationKeyInfo()
        dummy_activation_key = dummy_activation_key_info.create().key
        dummy_recipient_list = ['joo2theeon@gamil.com']

        send_verification_mail(
            activation_key=dummy_activation_key,
            recipient_list=dummy_recipient_list,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, dummy_recipient_list)


class SignupViewTest(TestCase):
    client = Client()
    dummy_email = 'dummy@example.com'
    dummy_nickname = 'dummy'
    dummy_password = 'password'
    dummy_instrument = 'instrument'

    def test_is_user_created(self):
        response = self.client.post(reverse('user:signup'), {
            'email': self.dummy_email,
            'nickname': self.dummy_nickname,
            'password1': self.dummy_password,
            'password2': self.dummy_password,
            'instrument': self.dummy_instrument
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(response.json()['email'], self.dummy_email)
        self.assertEqual(response.json()['nickname'], self.dummy_nickname)
        self.assertEqual(response.json()['instrument'], self.dummy_instrument)

    def test_send_verification_mail(self):
        self.client.post(reverse('user:signup'), {
            'email': self.dummy_email,
            'nickname': self.dummy_nickname,
            'password1': self.dummy_password,
            'password2': self.dummy_password,
            'instrument': self.dummy_instrument
        })
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.dummy_email])


class ActivateUserView(TestCase):
    client = Client()

    def test_activation_link(self):
        dummy_activation_key_info = DummyActivationKeyInfo().create()
        dummy_recipient_list = ['joo2theeon@gamil.com']

        send_verification_mail(
            activation_key=dummy_activation_key_info.key,
            recipient_list=dummy_recipient_list,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, dummy_recipient_list)

        response = self.client.get(reverse('user:activate'), {
            'activation_key': dummy_activation_key_info.key,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(User.objects.first().is_active, True)

        expected_data = {
            'user': UserSerializer(dummy_activation_key_info.user).data,
            'is_active': True
        }
        expected_data_json = JSONRenderer().render(expected_data)
        self.assertEqual(response.content, expected_data_json)

    def test_expires_at_working(self):
        expires_at = datetime.now()
        dummy_activation_key_info = DummyActivationKeyInfo(expires_at=expires_at).create()

        self.client.get(reverse('user:activate'), {
            'activation_key': dummy_activation_key_info.key,
        })
        self.assertRaisesMessage(APIException, 'activation_key 의 기한이 만료되었습니다.')


class LoginViewTest(TransactionTestCase):
    client = Client()

    def test_login_token(self):
        user = DummyUser().create()
        user.is_active = True
        user.save()

        response = self.client.post(reverse('user:login'), {
            'email': DummyUser().EMAIL,
            'password': DummyUser().PASSWORD,
        })
        expected_data = {
            'token': user.token,
            'user': UserSerializer(user).data,
        }
        expected_data_json = JSONRenderer().render(expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected_data_json)

    def test_invalid_credentials_response(self):
        response = self.client.post(reverse('user:login'), {
            'email': DummyUser().EMAIL,
            'password': DummyUser().PASSWORD,
        })
        expected_data = {
            'message': 'Invalid credentials'
        }
        expected_data_json = JSONRenderer().render(expected_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.content, expected_data_json)
