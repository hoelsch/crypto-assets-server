from django.contrib.auth.models import User
from django.test import Client, TestCase


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.password = "test_pw1234"
        self.email = "test@test.com"

    def test_successful_register(self):
        response = self.client.post("/register", {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "email": self.email
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")

        user = User.objects.get(username=self.username)

        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)

    def test_register_with_missing_username(self):
        response = self.client.post("/register", {
            "password1": self.password,
            "password2": self.password,
            "email": self.email
        })

        self.assertEqual(response.status_code, 400)

    def test_register_with_missing_email(self):
        response = self.client.post("/register", {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
        })

        self.assertEqual(response.status_code, 400)

    def test_register_with_missing_password(self):
        response = self.client.post("/register", {
            "username": self.username,
            "email": self.email
        })

        self.assertEqual(response.status_code, 400)

    def test_register_with_invalid_username(self):
        response = self.client.post("/register", {
            "username": "",
            "password1": self.password,
            "password2": self.password,
            "email": self.email
        })

        self.assertEqual(response.status_code, 400)

    def test_register_with_invalid_email(self):
        response = self.client.post("/register", {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "email": "invalid format"
        })

        self.assertEqual(response.status_code, 400)

    def test_register_with_invalid_password(self):
        response = self.client.post("/register", {
            "username": self.username,
            "password1": "password",
            "password2": "password",
            "email": self.email
        })

        self.assertEqual(response.status_code, 400)

    def test_register_passwords_not_match(self):
        response = self.client.post("/register", {
            "username": self.username,
            "password1": self.password,
            "password2": self.password + "2",
            "email": self.email
        })

        self.assertEqual(response.status_code, 400)

    def test_register_username_already_exists(self):
        response = self.client.post("/register", {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "email": self.email
        })

        response = self.client.post("/register", {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "email": "some.new@mail.com"
        })

        self.assertEqual(response.status_code, 400)

    def test_register_email_already_exists(self):
        response = self.client.post("/register", {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "email": self.email
        })

        response = self.client.post("/register", {
            "username": "new_user",
            "password1": self.password,
            "password2": self.password,
            "email": self.email
        })

        self.assertEqual(response.status_code, 400)
