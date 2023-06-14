from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Crypto


@require_http_methods(["GET"])
def cryptos(request):
    if not request.user.is_authenticated:
        return JsonResponse({}, status=401)

    queryset = Crypto.objects.all()

    cryptos = []
    for crypto in queryset:
        cryptos.append(
            {
                "name": crypto.name,
                "abbreviation": crypto.abbreviation,
                "iconurl": crypto.iconurl,
            }
        )

    return JsonResponse({"cryptos": cryptos})
