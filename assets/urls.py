from django.urls import path

from .views import AssetListView, AssetManagementView

urlpatterns = [
    path("user/<int:user_id>/assets", AssetListView.as_view(), name="list-assets"),
    path(
        "user/<int:user_id>/assets/<crypto>",
        AssetManagementView.as_view(),
        name="create-update-assets",
    ),
]
