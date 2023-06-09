from django.http import JsonResponse
from django.shortcuts import render

from .models import Crypto


def cryptos(request):
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
