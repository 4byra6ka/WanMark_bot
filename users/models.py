from django.contrib.auth.models import AbstractUser
from django.db import models

from bot.models import BotUser


class User(AbstractUser):
    email = None
    telegram = models.OneToOneField(BotUser, on_delete=models.SET_NULL, null=True, blank=True)
    EMAIL_FIELD = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

