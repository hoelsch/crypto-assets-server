from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from .forms import CustomUserCreationForm
from crypto_assets_server.errors import InvalidJsonErrorResponse


@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return InvalidJsonErrorResponse()

    form = CustomUserCreationForm(data)

    if not form.is_valid():
        return JsonResponse({"error": form.errors}, status=400)

    form.save()

    return JsonResponse({"message": "Successfully created user"}, status=201)


@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as err:
        return InvalidJsonErrorResponse()

    form = AuthenticationForm(request, data=data)

    if not form.is_valid():
        return JsonResponse({"error": "Invalid username or password"}, status=400)

    user = form.get_user()
    login(request, user)

    return JsonResponse({"message": "Successfully logged in", "user_id": user.id})


@require_http_methods(["POST"])
def logout_user(request):
    logout(request)

    return JsonResponse({"message": "Successfully logged out"})
