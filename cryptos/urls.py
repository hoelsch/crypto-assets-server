from django.urls import path

from . import views

urlpatterns = [path("cryptos", views.cryptos, name="cryptos")]
