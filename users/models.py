from django.contrib.auth.models import AbstractUser
from django.db import models

from bot.models import BotUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    email = None
    # username = models.CharField(unique=True, max_length=25, verbose_name='Имя пользователя')
    telegram = models.OneToOneField(BotUser, on_delete=models.SET_NULL, null=True, blank=True)
    EMAIL_FIELD = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
