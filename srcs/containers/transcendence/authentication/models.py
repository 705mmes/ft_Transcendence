from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    request = models.ForeignKey(User, related_name='request', on_delete=models.CASCADE)
    pending = models.ForeignKey(User, related_name='pending', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('request', 'pending')


class FriendList(models.Model):
    friends = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)