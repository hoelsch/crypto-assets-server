from django.http import JsonResponse
from django.views import View

from .models import Asset


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
