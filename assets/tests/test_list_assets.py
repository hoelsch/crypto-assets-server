from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from assets.models import Asset
from cryptos.models import Crypto


class ListAssetsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        Crypto.objects.create(
            name="bitcoin", abbreviation="BTC", iconurl="https://test.com/test1.png"
        )
        Crypto.objects.create(
            name="ethereum", abbreviation="ETH", iconurl="https://test.com/test2.png"
        )

        self.user = User.objects.create_user(
            username="test", password="Test1234", email="test@test.com"
        )
        self.client.login(username=self.user.username, password="Test1234")

        bitcoin = Crypto.objects.get(name="bitcoin")
        Asset.objects.create(user=self.user, crypto=bitcoin, amount=10.5)
        ethereum = Crypto.objects.get(name="ethereum")
        Asset.objects.create(user=self.user, crypto=ethereum, amount=3)

    def test_list_assets_returns_correct_data(self):
        response = self.client.get(
            reverse("list-assets", kwargs={"user_id": self.user.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()
        assets = json_data["assets"]

        expected_assets = [
            {
                "crypto_name": "bitcoin",
                "user_id": self.user.id,
                "amount": 10.5,
                "abbreviation": "BTC",
                "iconurl": "https://test.com/test1.png",
            },
            {
                "crypto_name": "ethereum",
                "user_id": self.user.id,
                "amount": 3,
                "abbreviation": "ETH",
                "iconurl": "https://test.com/test2.png",
            },
        ]

        self.assertListEqual(assets, expected_assets)

    def test_list_assets_with_empty_result(self):
        Asset.objects.all().delete()
        response = self.client.get(
            reverse("list-assets", kwargs={"user_id": self.user.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()
        assets = json_data["assets"]

        self.assertListEqual(assets, [])

    def test_user_must_be_logged_in_to_list_assets(self):
        self.client.logout()
        response = self.client.get(
            reverse("list-assets", kwargs={"user_id": self.user.id})
        )

        self.assertContains(response, "error", status_code=401)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_user_cannot_list_assets_of_other_users(self):
        another_user = User.objects.create_user(
            username="new_user", password="Test1234", email="new_user@test.com"
        )
        self.client.login(username=another_user.username, password="Test1234")

        response = self.client.get(
            reverse("list-assets", kwargs={"user_id": self.user.id})
        )

        self.assertContains(response, "error", status_code=403)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_list_assets_only_allows_get_requests(self):
        http_methods = ["post", "patch", "put", "delete"]

        for method in http_methods:
            response = self.client.generic(
                method, reverse("list-assets", kwargs={"user_id": self.user.id})
            )
            self.assertEqual(response.status_code, 405)
