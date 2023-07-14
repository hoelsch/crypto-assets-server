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
        self.client.login(username=self.user.username, password="Test1234")

        self.asset = Asset.objects.create(crypto=crypto, user=self.user, amount=1)

    def _update_asset(self, crypto_name, request_data):
        response = self.client.put(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": crypto_name},
            ),
            data=json.dumps(request_data),
            content_type="application/json",
        )

        return response

    def test_update_existing_asset(self):
        crypto_name = "bitcoin"
        new_amount = 1.2

        response = self._update_asset(crypto_name, {"amount": new_amount})

        expected_json = {
            "message": f"Successfully added {new_amount} bitcoin to assets",
            "crypto": "bitcoin",
            "new_amount": new_amount,
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertDictEqual(response.json(), expected_json)

        asset = Asset.objects.get(user=self.user, crypto__name=crypto_name)

        self.assertEqual(asset.amount, new_amount)

    def test_new_asset_created_if_not_existing(self):
        self.asset.delete()

        crypto_name = "bitcoin"
        new_amount = 1.2

        response = self._update_asset(crypto_name, {"amount": new_amount})

        expected_json = {
            "message": f"Successfully added {new_amount} bitcoin to assets",
            "crypto": "bitcoin",
            "new_amount": new_amount,
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertDictEqual(response.json(), expected_json)

        asset = Asset.objects.get(user=self.user, crypto__name=crypto_name)

        self.assertEqual(asset.amount, new_amount)

    def test_update_asset_fails_for_unsupported_crypto(self):
        response = self._update_asset("unsupported_coin", {"amount": 1234})

        self.assertContains(response, "error", status_code=404)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_update_asset_fails_for_invalid_request_data(self):
        test_cases = [
            {"amount": "invalid_value"},
            {"invalid_field": 1},
            {},
        ]

        for data in test_cases:
            response = self._update_asset("bitcoin", data)

            self.assertContains(response, "error", status_code=400)
            self.assertEqual(response["Content-Type"], "application/json")

    def test_update_asset_fails_if_user_not_logged_in(self):
        self.client.logout()

        response = self._update_asset("bitcoin", {"amount": 1})

        self.assertContains(response, "error", status_code=401)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_user_cannot_update_asset_of_other_users(self):
        another_user = User.objects.create_user(
            username="new_user", password="Test1234", email="new_user@test.com"
        )
        self.client.login(username=another_user.username, password="Test1234")

        response = self._update_asset("bitcoin", {"amount": 1})

        self.assertContains(response, "error", status_code=403)
        self.assertEqual(response["Content-Type"], "application/json")
