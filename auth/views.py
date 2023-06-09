from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import CustomUserCreationForm


@require_http_methods(["POST"])
def register_user(request):
    form = CustomUserCreationForm(request.POST)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    form.save()

    return JsonResponse({"message": "Successfully created user"}, status=201)


@require_http_methods(["POST"])
def login_user(request):
    form = AuthenticationForm(request, data=request.POST)

    if not form.is_valid():
        return JsonResponse({"error": "Invalid username or password"}, status=400)

    user = form.get_user()
    login(request, user)

    return JsonResponse({"message": "Successfully logged in", "user_id": user.id})


@require_http_methods(["POST"])
def logout_user(request):
    logout(request)

    return JsonResponse({"message": "Successfully logged out"})
