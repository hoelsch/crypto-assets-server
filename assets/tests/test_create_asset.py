from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
import json

from assets.models import Asset
from cryptos.models import Crypto


class CreateAssetTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        Crypto.objects.create(
            name="bitcoin", abbreviation="BTC", iconurl="https://test.com/test1.png"
        )

        self.user = User.objects.create_user(
            username="test", password="Test1234", email="test@test.com"
        )
        self.client.login(username=self.user.username, password="Test1234")

    def _create_asset(self, crypto_name, request_data):
        response = self.client.post(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": crypto_name},
            ),
            data=json.dumps(request_data),
            content_type="application/json",
        )

        return response

    def test_create_new_asset(self):
        crypto_name = "bitcoin"
        amount = 1.5

        response = self._create_asset(crypto_name, {"amount": amount})

        expected_json = {
            "message": f"Successfully added {amount} bitcoin to assets",
            "crypto": "bitcoin",
            "new_amount": amount,
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertDictEqual(response.json(), expected_json)

        asset = Asset.objects.get(user=self.user, crypto__name=crypto_name)

        self.assertEqual(asset.amount, amount)

    def test_increase_amount_of_existing_asset(self):
        crypto = Crypto.objects.get(name="bitcoin")
        Asset.objects.create(crypto=crypto, user=self.user, amount=1)

        response = self._create_asset("bitcoin", {"amount": 1.5})

        expected_json = {
            "message": "Successfully added 1.5 bitcoin to assets",
            "crypto": "bitcoin",
            "new_amount": 2.5,
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertDictEqual(response.json(), expected_json)

        asset = Asset.objects.get(user=self.user, crypto__name="bitcoin")

        self.assertEqual(asset.amount, 2.5)

    def test_create_asset_fails_for_invalid_request_data(self):
        test_cases = [
            {"amount": "invalid_value"},
            {"invalid_field": 1},
            {},
        ]

        for data in test_cases:
            response = self._create_asset("bitcoin", data)

            self.assertContains(response, "error", status_code=400)
            self.assertEqual(response["Content-Type"], "application/json")

    def test_create_asset_fails_for_non_json_content_type(self):
        response = self.client.post(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
            ),
            data={"test": "a"},
        )

        self.assertContains(response, "error", status_code=400)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_create_asset_fails_for_unsupported_crypto(self):
        response = self._create_asset("unsupported_crypto", {"amount": 1})

        self.assertContains(response, "error", status_code=404)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_create_asset_fails_if_user_not_logged_in(self):
        self.client.logout()

        response = self._create_asset("bitcoin", {"amount": 1})

        self.assertContains(response, "error", status_code=401)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_user_cannot_create_asset_for_other_users(self):
        another_user = User.objects.create_user(
            username="new_user", password="Test1234", email="new_user@test.com"
        )
        self.client.login(username=another_user.username, password="Test1234")

        response = self._create_asset("bitcoin", {"amount": 1})

        self.assertContains(response, "error", status_code=403)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_user_cannot_increase_amount_of_asset_of_other_users(self):
        crypto = Crypto.objects.get(name="bitcoin")
        Asset.objects.create(crypto=crypto, user=self.user, amount=1)

        another_user = User.objects.create_user(
            username="new_user", password="Test1234", email="new_user@test.com"
        )
        self.client.login(username=another_user.username, password="Test1234")

        response = self._create_asset("bitcoin", {"amount": 1})

        self.assertContains(response, "error", status_code=403)
        self.assertEqual(response["Content-Type"], "application/json")
