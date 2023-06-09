from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from .models import Crypto


class CryptoTestCase(TestCase):
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

    def test_get_cryptos(self):
        response = self.client.get(reverse("cryptos"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        json_data = response.json()
        cryptos = json_data["cryptos"]

        self.assertListEqual(cryptos, self.cryptos)
