from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
import json


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.password = "test_pw1234"
        self.email = "test@test.com"

    def test_successful_register(self):
        response = self.client.post(
            reverse("register"),
            data=json.dumps(
                {
                    "username": self.username,
                    "password1": self.password,
                    "password2": self.password,
                    "email": self.email,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")

        user = User.objects.get(username=self.username)

        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)

    def test_register_with_missing_fields(self):
        test_cases = [
            {
                "password1": self.password,
                "password2": self.password,
                "email": self.email,
            },
            {
                "username": self.username,
                "password1": self.password,
                "password2": self.password,
            },
            {"username": self.username, "email": self.email},
        ]

        for data in test_cases:
            response = self.client.post(
                reverse("register"),
                data=json.dumps(data),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 400)

    def test_register_with_invalid_inputs(self):
        test_cases = [
            {
                "username": "",
                "password1": self.password,
                "password2": self.password,
                "email": self.email,
            },
            {
                "username": self.username,
                "password1": self.password,
                "password2": self.password,
                "email": "invalid format",
            },
            {
                "username": self.username,
                "password1": "password",
                "password2": "password",
                "email": self.email,
            },
            {
                "username": self.username,
                "password1": self.password,
                "password2": self.password + "2",
                "email": self.email,
            },
        ]

        for data in test_cases:
            response = self.client.post(
                reverse("register"),
                data=json.dumps(data),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 400)

    def test_register_duplicate_username(self):
        response = self.client.post(
            reverse("register"),
            data=json.dumps(
                {
                    "username": self.username,
                    "password1": self.password,
                    "password2": self.password,
                    "email": self.email,
                }
            ),
            content_type="application/json",
        )

        response = self.client.post(
            reverse("register"),
            data=json.dumps(
                {
                    "username": self.username,
                    "password1": self.password,
                    "password2": self.password,
                    "email": "some.new@mail.com",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_register_duplicate_email(self):
        response = self.client.post(
            reverse("register"),
            data=json.dumps(
                {
                    "username": self.username,
                    "password1": self.password,
                    "password2": self.password,
                    "email": self.email,
                }
            ),
            content_type="application/json",
        )

        response = self.client.post(
            reverse("register"),
            data=json.dumps(
                {
                    "username": "new_user",
                    "password1": self.password,
                    "password2": self.password,
                    "email": self.email,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
