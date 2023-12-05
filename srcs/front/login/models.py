from django.db import models

class User(models.Model):
    username = models.CharField(max_length=21)
    avatar = models.ImageField()
    is_online = models.BooleanField()

class Friendship(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
	friend_of = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')

class Match(models.Model):
	player_1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_1', null=True)
	player_2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_2', null=True)
	winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='winner', null=True)
	date = models.DateField()
