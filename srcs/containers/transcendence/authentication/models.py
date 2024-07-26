from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_connected = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.username
