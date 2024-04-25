from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True) 
    username = models.CharField(max_length=21)
    avatar = models.ImageField()
    is_online = models.BooleanField(null=True)

class Friendship(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
	friend_of = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')()
