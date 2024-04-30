import logging
from pprint import pprint

import telebot
from django.conf import settings
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from bot.middleware import CustomMiddleware

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

bot.setup_middleware(CustomMiddleware())


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message: Message):
    logger.info(f'{message}')
    pprint(f'{message}')
    text = 'Привет, тест'
    await bot.delete_message(message.chat.id, message.id)
    await bot.send_message(message.chat.id, text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)
