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

    def __str__(self):
        return f"{self.History1} - {self.History2}"


class GameLobby(models.Model):
    Player1 = models.ForeignKey(User, related_name='Player1', on_delete=models.CASCADE,  blank=True, null=True)
    Player2 = models.ForeignKey(User, related_name='Player2', on_delete=models.CASCADE,  blank=True, null=True)
    Name = models.CharField(blank=True)

    def __str__(self):
        return f"{self.Player1.Player.username} - {self.Player2.Player.username}"

