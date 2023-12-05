from django.db import models

class Test(models.Model):
    string = models.CharField(max_length=80)
    number = models.IntegerField()
    current_date = models.DateField()
