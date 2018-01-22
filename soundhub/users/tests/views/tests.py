from unittest import TestCase

from django.test import Client


class SignupViewTest(TestCase):
    def test_sign_up_using_password(self):
        c = Client()
        context = {
            "email": "test@test.com",
            "nickname": "testuser",
            "password1": "password",
            "password2": "password",
        }
        response = c.post('/user/signup/', context)

        self.assertEqual(response.status_code, 302)


