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
