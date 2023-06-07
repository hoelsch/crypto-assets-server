from django.test import Client, TestCase
from django.contrib.auth.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.password = "test_pw1234"
        self.email = "test@test.com"

        user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email
        )
        self.user_id = user.id

    def test_successful_login(self):
        response = self.client.post(
            "/login",
            {
                "username": self.username,
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("sessionid", response.cookies)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertDictContainsSubset({"user_id": self.user_id}, json_data)

    def test_login_with_wrong_password(self):
        response = self.client.post(
            "/login",
            {
                "username": self.username,
                "password": "wrong_password",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("sessionid", response.cookies)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertEqual(json_data["error"], "Invalid username or password")

    def test_login_with_non_existing_user(self):
        response = self.client.post(
            "/login",
            {
                "username": "non_existing_user",
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("sessionid", response.cookies)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertEqual(json_data["error"], "Invalid username or password")
