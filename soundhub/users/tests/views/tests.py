from unittest import TestCase

from django.contrib.auth import get_user_model
from django.test import Client

from users.models import Genre, Instrument

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

        email = "test@test.com"
        nickname = "testuser"
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

        self.assertEqual(response.status_code, 302)

        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.nickname, "testuser")

        rock = Genre.objects.get(pk=1)
        jazz = Genre.objects.get(pk=3)

        self.assertIn(rock, user.genre.all())
        self.assertIn(jazz, user.genre.all())

        guitar = Instrument.objects.get(pk=2)

        self.assertIn(guitar, user.instrument.all())
