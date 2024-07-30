from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# class FriendRequest(models.Model):
#     request = models.ForeignKey(User, related_name='request', on_delete=models.CASCADE, blank=True)
#     pending = models.ForeignKey(User, related_name='pending', on_delete=models.CASCADE, blank=True)
#
#     class Meta:
#         unique_together = ('request', 'pending')


class FriendList(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='user_1', on_delete=models.CASCADE, blank=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='user_2', on_delete=models.CASCADE, blank=True)

    # class Meta:
    #     unique_together = ('user1', 'user2')

    def username(self):
        return self.user1.username

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"
