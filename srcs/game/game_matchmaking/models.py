from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):

    class GameStatus(models.TextChoices):
        WAITING = 'WAITING'
        IN_PROGRESS = 'IN_PROGRESS'
        PAUSED = 'PAUSED'
        FINISHED = 'FINISHED'

    playerLeft = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playerLeft')
    playerRight = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playerRight')
    playerLeftScore = models.IntegerField(default=0)
    playerRightScore = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=GameStatus.choices, default=GameStatus.WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

class GameInvite(models.Model):
    class InviteStatus(models.TextChoices):
        PENDING = 'PENDING'
        ACCEPTED = 'ACCEPTED'
        DECLINED = 'DECLINED'
        CANCELLED = 'CANCELLED'
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=InviteStatus.choices, default=InviteStatus.PENDING)

