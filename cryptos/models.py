from django.db import models


class Crypto(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    iconurl = models.CharField(max_length=255)
