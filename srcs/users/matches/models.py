from django.db import models

class Match(models.Model):
	player_1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_1', null=True)
	player_2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_2', null=True)
	winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='winner', null=True)
	date = models.DateField()
