import asyncio
import logging

import telebot
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from telebot import util

from bot.main_bot import bot

logger = logging.getLogger(__name__)

telebot.logger.setLevel(settings.LOG_LEVEL)


class Command(BaseCommand):
    help = "Запускаем бота WanMark"

    def handle(self, *args, **options):
        try:
            asyncio.run(bot.infinity_polling(logger_level=settings.LOG_LEVEL, allowed_updates=util.update_types))
        except Exception as err:
            logger.error(f'Ошибка: {err}')
