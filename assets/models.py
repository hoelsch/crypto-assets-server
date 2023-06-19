from django.contrib.auth.models import User
from django.db import models

from cryptos.models import Crypto


class Asset(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
