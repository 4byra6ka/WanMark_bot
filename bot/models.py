from django.db import models
from django.utils.translation import gettext as _

NULLABLE = {'blank': True, 'null': True}


class BotUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(_('ID Telegram'), db_index=True, unique=True)
    username = models.CharField(_('Username'), max_length=150, **NULLABLE)
    full_name = models.CharField(_('Полное имя'), max_length=255, **NULLABLE)
    status_active = models.BooleanField(_('Статус'), default=True)
    create_date = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    last_change_date = models.DateTimeField(_('Дата последнего изменения'), auto_now=True)

    def __str__(self):
        return f"@{self.username}({self.telegram_id})"

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class MenuActions(models.Model):
    bot_user = models.OneToOneField("BotUser", on_delete=models.CASCADE, verbose_name='Пользователь бота', **NULLABLE)
    main = models.CharField(_('Главное меню'), max_length=255, **NULLABLE)
    sub = models.CharField(_('Подменю'), max_length=255, **NULLABLE)
    door = models.CharField(_('Карточка двери'), max_length=255, **NULLABLE)
    message_id = models.CharField(_('ID сообщения'), max_length=255, **NULLABLE)
    media_message_id = models.TextField(**NULLABLE)

    def __str__(self):
        return f"main: {self.main}, sub: {self.telegram_id}, door:{self.door}"
