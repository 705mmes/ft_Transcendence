from datetime import datetime
from math import trunc

from django.db import models
from django.conf import settings
from authentication.models import User
from django.utils.timezone import now


class GameHistory(models.Model):
    History1 = models.ForeignKey(User, related_name='History1', on_delete=models.CASCADE,  blank=True, null=True)
    History2 = models.ForeignKey(User, related_name='History2', on_delete=models.CASCADE,  blank=True, null=True)
    Score1 = models.IntegerField()
    Score2 = models.IntegerField()
    ffed1 = models.BooleanField()
    ffed2 = models.BooleanField()

    def __str__(self):
        return f"{self.History1} - {self.History2}"


class GameLobby(models.Model):
    Player1 = models.ForeignKey(User, related_name='Player1', on_delete=models.CASCADE,  blank=True, null=True)
    Player2 = models.ForeignKey(User, related_name='Player2', on_delete=models.CASCADE,  blank=True, null=True)
    Name = models.CharField(blank=True)

    def __str__(self):
        return f"{self.Player1.Player.username} - {self.Player2.Player.username}"

class TournamentLobby(models.Model):
    P1 = models.ForeignKey(User, related_name='P1', on_delete=models.CASCADE,  blank=True, null=True)
    P2 = models.ForeignKey(User, related_name='P2', on_delete=models.CASCADE,  blank=True, null=True)
    P3 = models.ForeignKey(User, related_name='P3', on_delete=models.CASCADE,  blank=True, null=True)
    P4 = models.ForeignKey(User, related_name='P4', on_delete=models.CASCADE,  blank=True, null=True)
    Name = models.CharField(blank=True)
    is_full = models.BooleanField(default=False)
    player_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.P1.Player.username} - {self.P2.Player.username}"

