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
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner', null=True, blank=True)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
    connection_time = models.DateTimeField(null=True, blank=True)
    disconnection_time = models.DateTimeField(null=True, blank=True)
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

class Tournament(models.Model):
    class TournamentStatus(models.TextChoices):
        WAITING = 'WAITING'
        IN_PROGRESS = 'IN_PROGRESS'
        FINISHED = 'FINISHED'

    tournament_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournament_winner', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=TournamentStatus.choices, default=TournamentStatus.WAITING)

class UserTournament(models.Model):
    class UserStatus(models.TextChoices):
        PLAYING = 'PLAYING'
        ELIMINATED = 'ELIMINATED'
        FINISHED = 'FINISHED'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=UserStatus.choices, default=UserStatus.PLAYING)
    
