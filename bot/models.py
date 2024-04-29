from django.db import models
from django.utils.translation import gettext as _

NULLABLE = {'blank': True, 'null': True}


class BotUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(_('ID Telegram'), db_index=True, unique=True)
    username = models.CharField(_('Username'), max_length=150, **NULLABLE)
    full_name = models.CharField(_('Полное имя'), max_length=255, **NULLABLE)

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'
