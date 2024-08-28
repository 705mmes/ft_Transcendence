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
        return f"{self.History1.username} - {self.History2.username}"

class PosPlayer(models.Model):
    Player = models.ForeignKey(User, related_name='Player', on_delete=models.CASCADE,  blank=True, null=True)
    posX = models.IntegerField(blank=True, null=True, default=0)
    posY = models.IntegerField(blank=True, null=True, default=1080 / 2 - 233 / 2)
    dir = models.CharField(blank=True, default="stop")
    time_start = models.DateTimeField(default=now, blank=True)
    time_end = models.DateTimeField(default=now, blank=True)

    def set_to_player1(self):
        self.posX = 0
        self.posY = 0
        # self.posY = 1080 / 2 - 233 / 2

    def set_to_player2(self):
        self.posX = 2040 - 77
        self.posY = 0
        # self.posY = 1080 / 2 - 233 / 2


class GameLobby(models.Model):
    Player1 = models.ForeignKey(User, related_name='Player1', on_delete=models.CASCADE,  blank=True, null=True)
    # Player1 = models.ForeignKey(PosPlayer, related_name='Player1', on_delete=models.CASCADE,  blank=True, null=True)
    # Player1_posX = models.IntegerField(blank=True, null=True, default=0)
    # Player1_posY = models.IntegerField(blank=True, null=True, default=1080/2 - 233/2)
    # Player1_dir = models.CharField(blank=True, default="stop")
    Player2 = models.ForeignKey(User, related_name='Player2', on_delete=models.CASCADE,  blank=True, null=True)
    # Player2 = models.ForeignKey(PosPlayer, related_name='Player2', on_delete=models.CASCADE,  blank=True, null=True)
    # Player2_posX = models.IntegerField(blank=True, null=True, default=2040 - 74)
    # Player2_posY = models.IntegerField(blank=True, null=True, default=1080/2 - 233/2)
    # Player2_dir = models.CharField(blank=True, default="stop")
    Name = models.CharField(blank=True)

    def __str__(self):
        return f"{self.Player1.Player.username} - {self.Player2.Player.username}"

