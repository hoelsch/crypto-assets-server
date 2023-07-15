from django.http import JsonResponse


class InvalidJsonErrorResponse(JsonResponse):
    def __init__(self):
        super().__init__({"error": "Invalid JSON data in request body"}, status=400)
