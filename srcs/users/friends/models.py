from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests_sent")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests_received")
