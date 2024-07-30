from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class FriendRequest(models.Model):
    request = models.ForeignKey(User, related_name='request', on_delete=models.CASCADE)
    pending = models.ForeignKey(User, related_name='pending', on_delete=models.CASCADE)



# class FriendList(models.Model):
#     friends = models.ForeignKey(User, on_delete=models.CASCADE,related_name='friends', blank=True)
#     class Meta:
#         unique_together = ()

