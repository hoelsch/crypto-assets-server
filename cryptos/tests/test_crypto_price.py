from unittest.mock import patch
import requests
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from cryptos.models import Crypto


class CryptoPriceTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        Crypto.objects.create(
            name="bitcoin", abbreviation="BTC", iconurl="https://test.com/test1.png"
        )

        user = User.objects.create_user(
            username="test", password="Test1234", email="test@test.com"
        )
        self.client.login(username=user.username, password="Test1234")

    def _get_crypto_price(self, crypto):
        response = self.client.get(reverse("crypto-price", kwargs={"crypto": crypto}))

        return response

    @patch("requests.get")
    def test_get_crypto_price(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"price": "1000"}

        response = self._get_crypto_price("bitcoin")

        expected_json = {"crypto_name": "bitcoin", "price": "1000", "unit": "EUR"}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertDictEqual(response.json(), expected_json)

    @patch("requests.get")
    def test_get_crypto_price_fails_if_request_to_remote_api_fails(self, mock_request):
        mock_request.return_value.status_code = 500

        response = self._get_crypto_price("bitcoin")

        self.assertContains(response, "error", status_code=500)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_get_crypto_price_fails_for_unsupported_crypto(self):
        response = self._get_crypto_price("unsupported_crypto")

        self.assertContains(response, "error", status_code=404)
        self.assertEqual(response["Content-Type"], "application/json")

    @patch("requests.get")
    def test_get_crypto_price_fails_for_timeout(self, mock_request):
        mock_request.side_effect = requests.Timeout()

        response = self._get_crypto_price("bitcoin")

        self.assertContains(response, "error", status_code=504)
        self.assertEqual(response["Content-Type"], "application/json")

    @patch("requests.get")
    def test_get_crypto_price_fails_for_request_exception(self, mock_request):
        mock_request.side_effect = requests.RequestException()

        response = self._get_crypto_price("bitcoin")

        self.assertContains(response, "error", status_code=500)
        self.assertEqual(response["Content-Type"], "application/json")
