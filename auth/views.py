from django.http import JsonResponse

from .forms import CustomUserCreationForm

def register(request):
    form = CustomUserCreationForm(request.POST)

    if not form.is_valid():
        # TODO: implement error case
        pass

    form.save()

    return JsonResponse({"message": "Successfully created user"}, status=201)
