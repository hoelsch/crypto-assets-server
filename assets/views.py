from django.http import JsonResponse
from django.views import View
import json

from .models import Asset
from .forms import AssetCreateUpdateForm
from cryptos.models import Crypto
from crypto_assets_server.mixins import CustomLoginRequiredMixin
from crypto_assets_server.mixins import UserAccessOwnResourcesMixin


class AssetListView(CustomLoginRequiredMixin, UserAccessOwnResourcesMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = Asset.objects.filter(user=request.user)
        assets = []

        for asset in queryset:
            assets.append(
                {
                    "crypto_name": asset.crypto.name,
                    "user_id": asset.user.id,
                    "amount": asset.amount,
                }
            )

        return JsonResponse({"assets": assets})


class AssetManagementView(CustomLoginRequiredMixin, UserAccessOwnResourcesMixin, View):
    def post(self, request, *args, **kwargs):
        return self._create_or_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self._create_or_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        crypto, err = self._validate_and_return_crypto(**kwargs)
        if err is not None:
            return err

        try:
            asset = Asset.objects.get(user=request.user, crypto=crypto)
            asset.delete()
        except Asset.DoesNotExist:
            return JsonResponse(
                {
                    "error": f"Cannot delete asset '{crypto.name}' because it does not exist"
                },
                status=404,
            )

        return JsonResponse({"message": f"Successfully deleted asset {crypto.name}"})

    def _create_or_update(self, request, *args, **kwargs):
        form, err = self._validate_and_return_request_data(request.body)
        if err is not None:
            return err

        crypto, err = self._validate_and_return_crypto(**kwargs)
        if err is not None:
            return err

        amount = form.cleaned_data["amount"]

        asset, _ = Asset.objects.get_or_create(
            user=request.user, crypto=crypto, defaults={"amount": 0}
        )

        if request.method == "POST":
            asset.amount += amount
        elif request.method == "PUT":
            asset.amount = amount

        asset.save()

        return JsonResponse(
            {
                "message": f"Successfully added {amount} {crypto.name} to assets",
                "crypto": crypto.name,
                "new_amount": asset.amount,
            }
        )

    def _validate_and_return_request_data(self, body):
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return None, JsonResponse(
                {"error": "Invalid JSON data in request body"}, status=400
            )

        form = AssetCreateUpdateForm(data)
        if not form.is_valid():
            return None, JsonResponse({"error": form.errors}, status=400)

        return form, None

    def _validate_and_return_crypto(self, **kwargs):
        crypto_name = kwargs.get("crypto")

        if not crypto_name:
            return JsonResponse({"error": "Crypto parameter is missing"}, status=400)

        try:
            crypto = Crypto.objects.get(name=crypto_name)
        except Crypto.DoesNotExist:
            return None, JsonResponse(
                {"error": f"Crypto {crypto_name} is not supported"}, status=400
            )

        return crypto, None
