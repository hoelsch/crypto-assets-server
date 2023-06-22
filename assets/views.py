from django.http import JsonResponse
from django.views import View
import json

from .models import Asset
from .forms import AssetCreateUpdateForm
from cryptos.models import Crypto


class AssetListView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"error": "Only logged in users can list assets."}, status=401
            )

        user_id = kwargs["user_id"]

        if not request.user.id == user_id:
            return JsonResponse(
                {
                    "error": (
                        f"User {request.user.id} is not allowed to list assets of user {user_id}. "
                        f"Users can only list their own assets"
                    )
                },
                status=403,
            )

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


class AssetCreateUpdateView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"error": "Only logged in users can create assets."}, status=401
            )

        user_id = kwargs["user_id"]

        if not request.user.id == user_id:
            return JsonResponse(
                {
                    "error": (
                        f"User {request.user.id} is not allowed to create assets for user {user_id}. "
                        f"Users can only create assets for themselves"
                    )
                },
                status=403,
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON data in request body"}, status=400
            )

        form = AssetCreateUpdateForm(data)
        if not form.is_valid():
            return JsonResponse({"error": form.errors}, status=400)

        amount = data["amount"]
        crypto_name = kwargs["crypto"]

        try:
            crypto = Crypto.objects.get(name=crypto_name)
        except Crypto.DoesNotExist:
            return JsonResponse(
                {"error": f"Crypto {crypto_name} is not supported"}, status=400
            )

        try:
            asset = Asset.objects.get(user=request.user, crypto=crypto)
            asset.amount += amount
            asset.save()
            new_amount = asset.amount
        except Asset.DoesNotExist:
            Asset.objects.create(user=request.user, crypto=crypto, amount=amount)
            new_amount = amount

        return JsonResponse(
            {
                "message": f"Successfully added {amount} {crypto_name} to assets",
                "crypto": crypto_name,
                "new_amount": new_amount,
            }
        )
