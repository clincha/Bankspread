from django.db import models


# Create your models here.


class Starling(models.Model):
    access_token = models.CharField(max_length=4000)
    refresh_token = models.CharField(max_length=4000)
    token_expires = models.DateTimeField()
