from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Crypto


@require_http_methods(["GET"])
def cryptos(request):
    """
    View function that returns a JSON response containing a list of supported cryptocurrencies.
    Only authenticated users are allowed to access this view.

    Returns:
        JsonResponse: JSON response containing a list of supported cryptocurrencies.
            The response structure is {"cryptos": [...]}.
            Each cryptocurrency in the list is represented as a dictionary with keys "name",
            "abbreviation", and "iconurl".
    """
    if not request.user.is_authenticated:
        return JsonResponse({}, status=401)

    queryset = Crypto.objects.values("name", "abbreviation", "iconurl")
    result = list(queryset)

    return JsonResponse({"cryptos": result})
