from django.http import JsonResponse


class CustomLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        return super().dispatch(request, *args, **kwargs)


class UserAccessOwnResourcesMixin:
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        if request.user.id != user_id:
            return JsonResponse(
                {
                    "error": "User has no permissions to perform operations on resources of other users"
                },
                status=403,
            )

        return super().dispatch(request, *args, **kwargs)
