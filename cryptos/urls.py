from django.urls import path

from . import views

urlpatterns = [
    path("cryptos", views.CryptoListView.as_view(), name="cryptos"),
    path(
        "cryptos/<str:crypto>/price",
        views.CryptoPriceView.as_view(),
        name="crypto-price",
    ),
]
