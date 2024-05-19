import json
import logging
from enum import IntEnum, auto
from pprint import pprint

import telebot
from asgiref.sync import sync_to_async
from django.conf import settings
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import AdvancedCustomFilter
from telebot.asyncio_handler_backends import StatesGroup, State
from telebot.asyncio_storage import StateMemoryStorage
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto

from bot.filters import main_menu, root, sub_menu, door_card
from bot.keyboards import main_menu_kb, sub_menu_kb, door_card_kb, one_door_card_kb
from bot.middleware import CustomMiddleware
from bot.services.db_botuser_dao import update_or_create_menu_actions, get_menu_actions, get_image_title_door, \
    get_description_main_menu
from wanmark.models import MainMenuBot, SubMenuBot, DoorCardBot

bot = AsyncTeleBot(settings.TOKEN_BOT, state_storage=StateMemoryStorage(), parse_mode='HTML')
# bot.enable_saving_states(filename=f'{settings.MEDIA_ROOT}/.bot_states.pkl')
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

bot.setup_middleware(CustomMiddleware())


# class MenuActions(StatesGroup):
#     main = State()
#     sub = State()
#     door = State()


@bot.message_handler(commands=['help', 'start'])
async def handle_main_menu_list(message: Message):
    chat_id = message.chat.id
    status_menu_actions = await get_menu_actions(chat_id)
    # if not status_menu_actions:
    #     await update_or_create_menu_actions(chat_id, main=True, sub=True, door=True, message=True, media_message=True)
    try:
        if status_menu_actions['media_message_id'] or status_menu_actions['message_id']:
            media_message_list = []
            if status_menu_actions['message_id']:
                media_message_list.append(int(status_menu_actions['message_id']))
            if status_menu_actions['media_message_id']:
                [media_message_list.append(int(m_id)) for m_id in status_menu_actions['media_message_id'].split(',')]
            print(media_message_list)
            await bot.delete_messages(chat_id, media_message_list)
    except BaseException as err:
        logger.info(f'Ошибка удаления при /start {err}')

    text, wm_logo = await get_description_main_menu()
    message_tg = await bot.send_photo(chat_id, wm_logo, text, reply_markup=await main_menu_kb())
    await update_or_create_menu_actions(chat_id, main=True, sub=True, door=True, message_id=message_tg.message_id, media_message=True)
    # await update_or_create_menu_actions(chat_id, message_id=message_tg.message_id)
    await bot.delete_message(message.chat.id, message.id)


@bot.callback_query_handler(func=None, main_menu_config=main_menu.filter())
async def handle_sub_menu_list(call: CallbackQuery):
    chat_id = call.message.chat.id
    callback_data: dict = main_menu.parse(callback_data=call.data)
    main_menu_id: int = int(callback_data['m_id'])

    status_menu_actions = await get_menu_actions(chat_id)
    await update_or_create_menu_actions(chat_id, sub=True, door=True, media_message=True)

    main_menu_data: MainMenuBot = await MainMenuBot.objects.aget(id=main_menu_id)
    text = f'<b>{main_menu_data.name}</b>'
    if main_menu_data.title:
        text += f'\n{main_menu_data.title}'
    message_tg = await bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=status_menu_actions['message_id'],
        caption=text,
        reply_markup=await sub_menu_kb(main_menu_id)
    )
    await update_or_create_menu_actions(call.message.chat.id, main_id=main_menu_id, message_id=message_tg.message_id)


@bot.callback_query_handler(func=None, sub_menu_config=sub_menu.filter())
async def handle_door_menu_list(call: CallbackQuery):
    chat_id = call.message.chat.id
    callback_data: dict = sub_menu.parse(callback_data=call.data)
    sub_menu_id: int = int(callback_data['s_id'])

    status_menu_actions = await get_menu_actions(chat_id)
    if status_menu_actions['media_message_id']: # or status_menu_actions['message_id']:
        media_message_list = []
        # if status_menu_actions['message_id']:
        #     media_message_list.append(status_menu_actions['message_id'])
        if status_menu_actions['media_message_id']:
            [media_message_list.append(int(m_id)) for m_id in status_menu_actions['media_message_id'].split(',')]
        await bot.delete_messages(chat_id, media_message_list)
    await update_or_create_menu_actions(chat_id, door=True, message=True, media_message=True)

    sub_menu_data: SubMenuBot = await SubMenuBot.objects.aget(id=sub_menu_id)
    text = f'<b>{sub_menu_data.name}</b>'
    if sub_menu_data.title:
        text += f'\n{sub_menu_data.title}'

    message_tg = await bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=status_menu_actions['message_id'],
        caption=text,
        reply_markup=await door_card_kb(sub_menu_id=sub_menu_id, main_menu_id=int(status_menu_actions['main']))
    )
    await update_or_create_menu_actions(call.message.chat.id, sub_id=sub_menu_id, message_id=message_tg.message_id)


@bot.callback_query_handler(func=None, door_card_config=door_card.filter())
async def handle_door_menu(call: CallbackQuery):
    media_messages = []
    chat_id = call.message.chat.id
    callback_data: dict = door_card.parse(callback_data=call.data)
    door_card_id: int = int(callback_data['d_id'])
    status_menu_actions = await get_menu_actions(chat_id)
    if status_menu_actions['media_message_id']:
        media_message_list = [call.message.id]
        [media_message_list.append(int(m_id)) for m_id in status_menu_actions['media_message_id'].split(',')]
        await bot.delete_messages(call.message.chat.id, media_message_list)
        await update_or_create_menu_actions(call.message.chat.id, media_message=True)
    # else:
    #     await bot.delete_message(call.message.chat.id, call.message.id)

    door_card_data: DoorCardBot = await DoorCardBot.objects.aget(id=door_card_id)
    text = f'<b>{door_card_data.name}</b>'
    message_tg = await bot.edit_message_caption(
        chat_id=chat_id,
        message_id=status_menu_actions['message_id'],
        caption=text,
        # reply_markup=await one_door_card_kb(sub_menu_id=int(status_menu_actions['sub']), door_card_id=door_card_id)
    )
    if door_card_data.title:
        text += f'\n{door_card_data.title}'

    list_list_image = await get_image_title_door(door_card_data)
    for list_image in list_list_image:
        if len(list_image) > 1 and len(list_image) == 10 and len(list_list_image) > 1:
            media_group = await bot.send_media_group(call.message.chat.id, list_image)
            media_messages += [str(media_message1.message_id) for media_message1 in media_group]
            # media_message = ','.join([str(media_message1.message_id) for media_message1 in media_group])
        elif len(list_image) > 1 and len(list_image) == 10 and len(list_list_image) == 1:
            media_group = await bot.send_media_group(call.message.chat.id, list_image)
            media_messages += [str(media_message1.message_id) for media_message1 in media_group]
        elif len(list_image) > 1:
            media_group = await bot.send_media_group(call.message.chat.id, list_image)
            media_messages += [str(media_message1.message_id) for media_message1 in media_group]
        else:
            media_group = await bot.send_photo(call.message.chat.id, list_image[0])
            media_messages.append(str(media_group.message_id))
    media_messages = ','.join([str(media_id) for media_id in media_messages])

    message_sub_tg = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=await one_door_card_kb(sub_menu_id=int(status_menu_actions['sub']), door_card_id=door_card_id)
    )
    media_messages += f',{str(message_sub_tg.message_id)}'

    await update_or_create_menu_actions(
        call.message.chat.id,
        door_id=door_card_id,
        message_id=message_tg.message_id,
        media_message_id=media_messages)


@bot.callback_query_handler(func=None, root_config=root.filter())
async def handle_main_query(call: CallbackQuery):
    # Рефакторинг обновления
    chat_id = call.message.chat.id
    status_menu_actions = await get_menu_actions(chat_id)
    if status_menu_actions['media_message_id']:  # or status_menu_actions['message_id']:
        media_message_list = []
        # if status_menu_actions['message_id']:
        #     media_message_list.append(status_menu_actions['message_id'])
        if status_menu_actions['media_message_id']:
            [media_message_list.append(int(m_id)) for m_id in status_menu_actions['media_message_id'].split(',')]
        await bot.delete_messages(chat_id, media_message_list)
    await update_or_create_menu_actions(chat_id, main=True, sub=True, door=True, message=True, media_message=True)

    text, wm_logo = await get_description_main_menu()
    message_tg = await bot.edit_message_caption(
        chat_id=chat_id,
        message_id=status_menu_actions['message_id'],
        caption=text,
        reply_markup=await main_menu_kb()
    )
    await update_or_create_menu_actions(chat_id, message_id=message_tg.message_id)

