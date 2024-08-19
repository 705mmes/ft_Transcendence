from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='', default='images/Joever.jpg')
    is_connected = models.BooleanField(default=False)
    is_playing = models.BooleanField(default=False)
    in_research = models.BooleanField(default=True)

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
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user1', on_delete=models.CASCADE,  blank=True, null=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user2', on_delete=models.CASCADE, blank=True, null=True)

    # class Meta:
    #     unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1.username}"



class RepeatPasswordValidator():
    def validate(self, password, repeat_password,user=None):
        if password != repeat_password:
            raise ValidationError(
                ("Passwords do not match. try again."),
                code='password missmatch',
            )

class CustomMinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password is too short. It must contain at least 8 characters."),
                code='password too short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters."
        ) % {'min_length': self.min_length}