from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_picture = models.ImageField(default='images/smunio.jpg')
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE, blank=True)
    recipient = models.ForeignKey(User, related_name='recipient', on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('requester', 'recipient')

    def __str__(self):
        return f"{self.requester.username} - {self.recipient.username}"


class FriendList(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='user_1', on_delete=models.CASCADE, blank=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='user_2', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.user2.username}"
