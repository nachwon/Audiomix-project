from unittest import TestCase

from django.contrib.auth import get_user_model
from django.test import Client

from users.models import Genre, Instrument
from users.views import sign_up, sign_in, user_detail

User = get_user_model()


class SignupViewTest(TestCase):
    def setUp(self):
        Genre.objects.create(name="Rock")
        Genre.objects.create(name="Pop")
        Genre.objects.create(name="Jazz")
        Instrument.objects.create(name="Guitar")
        Instrument.objects.create(name="Bass")
        Instrument.objects.create(name="Drums")

        self.client = Client()

    def test_sign_up_using_password(self):
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
        response = self.client.post('/user/signup/', context)

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

        self.client = Client()

    def tearDown(self):
        User.objects.all().delete()

    def test_login_using_password(self):
        email = "login_test@test.com"
        password = "password"

        context = {
            "email": email,
            "password": password
        }

        response = self.client.post('/user/signin/', context)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/home/")
        self.assertEqual(response.resolver_match.func, sign_in)

    def test_logout(self):
        logged_in = self.client.login(email="login_test@test.com", password="password")

        user = User.objects.get(email="login_test@test.com")

        if logged_in:
            self.client.logout()


class UserViewTest(TestCase):
    def setUp(self):
        user = User(email="user_test@test.com",
                    nickname="user_testuser",
                    )
        user.set_password("password")
        user.save()

        user2 = User(email="user2_test@test.com",
                     nickname="user2_testuser",
                     )
        user2.set_password("password")
        user2.save()

        self.client = Client()

    def tearDown(self):
        User.objects.all().delete()

    def test_get_user_detail_page(self):
        logged_in = self.client.login(email="user_test@test.com", password="password")

        if logged_in:
            user = User.objects.get(email="user_test@test.com")

        response = self.client.get(f"/user/{user.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, user_detail)

    def test_follow_user_toggle(self):
        from_user = User.objects.get(email="user_test@test.com")
        to_user = User.objects.get(email="user2_test@test.com")

        self.client.login(email="user_test@test.com", password="password")

        response = self.client.post(f"/user/{to_user.pk}/follow/")

        self.assertEqual(response.status_code, 201)
        self.assertIn(from_user, to_user.followers.all())

        response2 = self.client.post(f"/user/{to_user.pk}/follow/")

        self.assertEqual(response2.status_code, 204)
        self.assertNotIn(from_user, to_user.followers.all())
