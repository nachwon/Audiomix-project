from unittest import TestCase

from django.contrib.auth import get_user_model
from django.test import Client

from users.models import Genre, Instrument
from users.views import sign_up

User = get_user_model()


class SignupViewTest(TestCase):
    def setUp(self):
        Genre.objects.create(name="Rock")
        Genre.objects.create(name="Pop")
        Genre.objects.create(name="Jazz")
        Instrument.objects.create(name="Guitar")
        Instrument.objects.create(name="Bass")
        Instrument.objects.create(name="Drums")

    def test_sign_up_using_password(self):
        c = Client()

        email = "signup_test@test.com"
        nickname = "signup_testuser"
        password1 = "password"
        password2 = "password"

        context = {
            "email": email,
            "nickname": nickname,
            "password1": password1,
            "password2": password2,
            "genre": ["1", "3"],
            "instrument": ["2"]
        }
        response = c.post('/user/signup/', context)

        user = User.objects.get(email=email)

        # View 테스트
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/home/")
        self.assertEqual(response.resolver_match.func, sign_up)

        # User 테스트
        self.assertEqual(user.email, "signup_test@test.com")
        self.assertEqual(user.nickname, "signup_testuser")

        # User 장르 테스트
        rock = Genre.objects.get(pk=1)
        jazz = Genre.objects.get(pk=3)

        self.assertIn(rock, user.genre.all())
        self.assertIn(jazz, user.genre.all())

        # User 악기 테스트
        guitar = Instrument.objects.get(pk=2)

        self.assertIn(guitar, user.instrument.all())


class LoginViewTest(TestCase):
    def setUp(self):
        user = User(email="login_test@test.com",
                    nickname="login_testuser",
                    )
        user.set_password("password")
        user.save()

    def test_login_using_password(self):
        c = Client()

        email = "login_test@test.com"
        password = "password"

        context = {
            "email": email,
            "password": password
        }

        response = c.post('/user/signin/', context)

        # print(response.content)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/home/")

