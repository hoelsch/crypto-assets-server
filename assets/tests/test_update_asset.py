from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
import json

from assets.models import Asset
from cryptos.models import Crypto


class UpdateAssetTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        crypto = Crypto.objects.create(
            name="bitcoin",
            abbreviation="BTC",
            iconurl="https://test.com/test1.png",
        )
        self.user = User.objects.create_user(
            username="test", password="Test1234", email="test@test.com"
        )
        self.asset = Asset.objects.create(crypto=crypto, user=self.user, amount=1)

        self.client.login(username=self.user.username, password="Test1234")

    def test_update_existing_asset(self):
        crypto_name = "bitcoin"
        new_amount = 1234
        body = json.dumps({"amount": new_amount})

        response = self.client.put(
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

        self.assertEqual(json_data["new_amount"], new_amount)
        self.assertEqual(json_data["crypto"], crypto_name)

        asset = Asset.objects.get(user=self.user, crypto__name=crypto_name)

        self.assertEqual(asset.amount, new_amount)

    def test_new_asset_created_if_not_existing(self):
        self.asset.delete()

        crypto_name = "bitcoin"
        new_amount = 1234
        body = json.dumps({"amount": new_amount})

        response = self.client.put(
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

        self.assertEqual(json_data["new_amount"], new_amount)
        self.assertEqual(json_data["crypto"], crypto_name)

        asset = Asset.objects.get(user=self.user, crypto__name=crypto_name)

        self.assertEqual(asset.amount, new_amount)

    def test_update_asset_fails_for_unsupported_crypto(self):
        response = self.client.put(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "unsupported_coin"},
            ),
            data=json.dumps({"amount": 1234}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)

    def test_update_asset_fails_for_invalid_request_data(self):
        test_cases = [
            "invalid json",
            json.dumps({"amount": "invalid_value"}),
            json.dumps({"invalid_field": 1}),
            json.dumps({}),
        ]

        for data in test_cases:
            response = self.client.put(
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

    def test_update_asset_fails_for_non_json_content(self):
        response = self.client.put(
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

    def test_update_asset_fails_if_user_not_logged_in(self):
        self.client.logout()

        body = json.dumps({"amount": 1})

        response = self.client.put(
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

    def test_user_cannot_update_asset_of_other_users(self):
        another_user = User.objects.create_user(
            username="new_user", password="Test1234", email="new_user@test.com"
        )
        self.client.login(username=another_user.username, password="Test1234")

        body = json.dumps({"amount": 1})

        response = self.client.put(
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
