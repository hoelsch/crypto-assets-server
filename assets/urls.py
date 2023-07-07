from django.urls import path

from .views import AssetListView, AssetManagementView

urlpatterns = [
    path("users/<int:user_id>/assets", AssetListView.as_view(), name="list-assets"),
    path(
        "users/<int:user_id>/assets/<str:crypto>",
        AssetManagementView.as_view(),
        name="manage-assets",
    ),
]
