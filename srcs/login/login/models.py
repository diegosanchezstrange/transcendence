from django.db import models

class User(models.Model):
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    is_online = models.BooleanField()
