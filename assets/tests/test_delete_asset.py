from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from assets.models import Asset
from cryptos.models import Crypto


class DeleteAssetTestCase(TestCase):
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

    def test_delete_asset(self):
        response = self.client.delete(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("message", json_data)

        with self.assertRaises(Asset.DoesNotExist):
            Asset.objects.get(user=self.user, crypto__name="bitcoin")

    def test_delete_fails_for_non_existing_asset(self):
        self.asset.delete()

        response = self.client.delete(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
            ),
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)

    def test_delete_asset_fails_if_user_not_logged_in(self):
        self.client.logout()

        response = self.client.delete(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
            ),
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)

    def test_user_cannot_delete_asset_of_other_users(self):
        another_user = User.objects.create_user(
            username="new_user", password="Test1234", email="new_user@test.com"
        )
        self.client.login(username=another_user.username, password="Test1234")

        response = self.client.delete(
            reverse(
                "manage-assets",
                kwargs={"user_id": self.user.id, "crypto": "bitcoin"},
            ),
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()

        self.assertIn("error", json_data)

        try:
            Asset.objects.get(user=self.user, crypto__name="bitcoin")
        except Asset.DoesNotExist:
            self.fail("User deleted asset of other user")
