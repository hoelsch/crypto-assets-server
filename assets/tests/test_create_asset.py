from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
import json

from assets.models import Asset
from cryptos.models import Crypto


class CreateAssetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.cryptos = [
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

        for crypto in self.cryptos:
            Crypto.objects.create(**crypto)

        self.user = User.objects.create_user(
            username="test", password="Test1234", email="test@test.com"
        )
        self.client.login(username=self.user.username, password="Test1234")

    def test_create_new_asset(self):
        crypto_name = "bitcoin"
        amount = 1.5

        body = json.dumps({"amount": amount})

        response = self.client.post(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": crypto_name},
            ),
            data=body,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("message", json_data)
        self.assertIn("new_amount", json_data)
        self.assertIn("crypto", json_data)

        self.assertEqual(json_data["new_amount"], amount)
        self.assertEqual(json_data["crypto"], crypto_name)

        asset = Asset.objects.get(user=self.user, crypto__name=crypto_name)

        self.assertEqual(asset.amount, amount)

    def test_increase_amount_of_existing_asset(self):
        crypto_name = "bitcoin"
        crypto = Crypto.objects.get(name=crypto_name)
        Asset.objects.create(crypto=crypto, user=self.user, amount=1)

        body = json.dumps({"amount": 1.5})

        response = self.client.post(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": crypto_name},
            ),
            data=body,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("message", json_data)
        self.assertIn("new_amount", json_data)
        self.assertIn("crypto", json_data)

        self.assertEqual(json_data["new_amount"], 2.5)
        self.assertEqual(json_data["crypto"], crypto_name)

        asset = Asset.objects.get(user=self.user, crypto__name=crypto_name)

        self.assertEqual(asset.amount, 2.5)

    def test_create_asset_fails_for_invalid_request_data(self):
        test_cases = [
            "invalid json",
            json.dumps({"amount": "invalid_value"}),
            json.dumps({"invalid_field": 1}),
            json.dumps({}),
        ]

        for data in test_cases:
            response = self.client.post(
                reverse(
                    "manage-assets",
                    kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
                ),
                data=data,
                content_type="application/json",
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response["Content-Type"], "application/json")

            json_data = response.json()

            self.assertIn("error", json_data)

    def test_create_asset_fails_for_non_json_content_type(self):
        response = self.client.post(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
            ),
            data={"test": "a"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)

    def test_create_asset_fails_for_unsupported_crypto(self):
        body = json.dumps({"amount": 1})

        response = self.client.post(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "unsupported_coin"},
            ),
            data=body,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)

    def test_create_asset_fails_if_user_not_logged_in(self):
        self.client.logout()

        body = json.dumps({"amount": 1})

        response = self.client.post(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
            ),
            data=body,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)

    def test_user_cannot_create_asset_for_other_users(self):
        another_user = User.objects.create_user(
            username="new_user", password="Test1234", email="new_user@test.com"
        )
        self.client.login(username=another_user.username, password="Test1234")

        body = json.dumps({"amount": 1})

        response = self.client.post(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
            ),
            data=body,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)

    def test_user_cannot_increase_amount_of_asset_of_other_users(self):
        crypto = Crypto.objects.get(name="bitcoin")
        Asset.objects.create(crypto=crypto, user=self.user, amount=1)

        another_user = User.objects.create_user(
            username="new_user", password="Test1234", email="new_user@test.com"
        )
        self.client.login(username=another_user.username, password="Test1234")

        body = json.dumps({"amount": 1})

        response = self.client.post(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
            ),
            data=body,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)
