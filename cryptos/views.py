import requests
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods

from .models import Crypto
from crypto_assets_server.mixins import CustomLoginRequiredMixin


class CryptoListView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        Returns a JSON response containing a list of supported cryptocurrencies.
        Only authenticated users are allowed to access this view.

        Returns:
            JsonResponse: JSON response containing a list of supported cryptocurrencies.
                The response structure is {"cryptos": [...]}.
                Each cryptocurrency in the list is represented as a dictionary with keys "name",
                "abbreviation", and "iconurl".
        """

        queryset = Crypto.objects.values("name", "abbreviation", "iconurl")
        result = list(queryset)

        return JsonResponse({"cryptos": result})


class CryptoPriceView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        crypto_name = kwargs.get("crypto")

        try:
            crypto = Crypto.objects.get(name=crypto_name)
        except Crypto.DoesNotExist:
            return JsonResponse(
                {"error": f"Crypto {crypto_name} does not exist"}, status=404
            )

        symbol = crypto.abbreviation + "EUR"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

        response = requests.get(url)

        if response.status_code != 200:
            return JsonResponse(
                {"error": f"Could not determine price of crypto {crypto_name}"},
                status=500,
            )

        json_data = response.json()
        price = json_data["price"]

        return JsonResponse({"crypto_name": crypto_name, "price": price, "unit": "EUR"})
