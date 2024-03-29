import requests
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods

from crypto_assets_server.mixins import CustomLoginRequiredMixin
from .models import Crypto


class CryptoListView(CustomLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        queryset = Crypto.objects.values("name", "abbreviation", "iconurl")
        result = list(queryset)

        return JsonResponse({"cryptos": result})


class CryptoPriceView(CustomLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        crypto_name = kwargs.get("crypto")

        try:
            crypto = Crypto.objects.get(name=crypto_name)
        except Crypto.DoesNotExist:
            return JsonResponse(
                {"error": f"Crypto {crypto_name} is not supported"}, status=404
            )

        symbol = crypto.abbreviation + "EUR"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

        try:
            response = requests.get(url, timeout=5)
        except requests.Timeout:
            return JsonResponse(
                {
                    "error": f"Timeout occurred while fetching the price of crypto {crypto_name}"
                },
                status=504,
            )
        except requests.RequestException as err:
            return JsonResponse(
                {
                    "error": f"An error occurred while fetching the price of crypto {crypto_name}: {str(err)}"
                },
                status=500,
            )

        if response.status_code != 200:
            return JsonResponse(
                {"error": f"Could not determine price of crypto {crypto_name}"},
                status=500,
            )

        json_data = response.json()
        price = json_data["price"]

        return JsonResponse({"crypto_name": crypto_name, "price": price, "unit": "EUR"})
