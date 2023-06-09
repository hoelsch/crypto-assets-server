from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class LogoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.password = "test_pw1234"
        self.email = "test@test.com"

        User.objects.create_user(
            username=self.username, password=self.password, email=self.email
        )

    def test_successful_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_logout_if_not_logged_in(self):
        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertFalse("_auth_user_id" in self.client.session)
