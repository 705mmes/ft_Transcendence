from math import trunc

from django.db import models
from django.conf import settings
from authentication.models import User


class GameHistory(models.Model):
    History1 = models.ForeignKey(User, related_name='History1', on_delete=models.CASCADE,  blank=True, null=True)
    History2 = models.ForeignKey(User, related_name='History2', on_delete=models.CASCADE,  blank=True, null=True)
    Score1 = models.IntegerField()
    Score2 = models.IntegerField()

    def __str__(self):
        return f"{self.History1.username} - {self.History2.username}"

class GameLobby(models.Model):
    Player1 = models.ForeignKey(User, related_name='Player1', on_delete=models.CASCADE,  blank=True, null=True)
    Player1_posX = models.IntegerField(blank=True, null=True, default=0)
    Player1_posY = models.IntegerField(blank=True, null=True, default=1080/2 - 233/2)
    Player2 = models.ForeignKey(User, related_name='Player2', on_delete=models.CASCADE,  blank=True, null=True)
    Player2_posX = models.IntegerField(blank=True, null=True, default=2040 - 74)
    Player2_posY = models.IntegerField(blank=True, null=True, default=1080/2 - 233/2)
    Name = models.CharField(blank=True)

    def __str__(self):
        return f"{self.Player1.username} - {self.Player2.username}"