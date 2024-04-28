from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=1000)
    connections = models.IntegerField(default=0)
