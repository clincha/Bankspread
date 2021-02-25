from django.db import models


# Create your models here.

class UserGoogle(models.Model):
    id = models.CharField(primary_key=True, max_length=250)
    email = models.CharField(max_length=4000)
    credentials = models.BinaryField()
