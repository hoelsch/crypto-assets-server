from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from cryptos.models import Crypto


class ListCryptosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.expected_cryptos = [
            {
                "name": "bitcoin",
                "abbreviation": "BTC",
                "iconurl": "https://test.com/test1.png",
            },
            {
                "name": "ethereum",
                "abbreviation": "ETH",
                "iconurl": "https://test.com/test2.png",
            },
        ]

        for crypto in self.expected_cryptos:
            Crypto.objects.create(**crypto)

        user = User.objects.create_user(
            username="test", password="Test1234", email="test@test.com"
        )
        self.client.login(username=user.username, password="Test1234")

    def test_list_cryptos_returns_correct_data(self):
        response = self.client.get(reverse("cryptos"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()
        cryptos = json_data["cryptos"]

        self.assertListEqual(cryptos, self.expected_cryptos)

    def test_list_cryptos_with_empty_result(self):
        Crypto.objects.all().delete()
        response = self.client.get(reverse("cryptos"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()
        cryptos = json_data["cryptos"]

        self.assertListEqual(cryptos, [])

    def test_user_must_be_logged_in_to_list_cryptos(self):
        self.client.logout()
        response = self.client.get(reverse("cryptos"))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)

    def test_list_cryptos_only_allows_get_requests(self):
        http_methods = ["post", "patch", "put", "delete"]

        for method in http_methods:
            response = getattr(self.client, method)(reverse("cryptos"))
            self.assertEqual(response.status_code, 405)
