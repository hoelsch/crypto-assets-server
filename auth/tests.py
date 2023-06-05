from django.contrib.auth.models import User
from django.test import Client, TestCase


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_successful_register(self):
        username = "test_user"
        password = "test_pw1234"
        email = "test@test.com"

        response = self.client.post("/register", {
            "username": username,
            "password1": password,
            "password2": password,
            "email": email
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")

        user = User.objects.get(username=username)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
