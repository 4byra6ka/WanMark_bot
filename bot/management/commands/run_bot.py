import asyncio
import logging

import telebot
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from telebot import util

from bot.filters import bind_filters
from bot.main_bot import bot, logger


class Command(BaseCommand):
    help = "Запускаем бота WanMark"

    def handle(self, *args, **options):
        try:
            asyncio.run(run_bot())
        except Exception as err:
            logger.error(f'Ошибка: {err}')


async def run_bot():
    bind_filters(bot)
    await bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("start", "Главное меню")
        ],
    )
    await bot.infinity_polling(logger_level=settings.LOG_LEVEL, allowed_updates=util.update_types)
