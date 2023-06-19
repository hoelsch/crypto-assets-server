from django.urls import path

from .views import AssetListView

urlpatterns = [
    path("user/<int:user_id>/assets", AssetListView.as_view(), name="list-assets")
]
