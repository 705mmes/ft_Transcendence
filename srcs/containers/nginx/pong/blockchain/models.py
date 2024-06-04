# myapp/models.py
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    eth_address = models.CharField(max_length=42)
    private_key = models.CharField(max_length=66)  # Length 66 for 0x-prefixed private key
    score = models.IntegerField(default=0)  # New score field

    def __str__(self):
        return self.name
