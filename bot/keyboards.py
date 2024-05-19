from enum import IntEnum, auto

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.filters import main_menu, sub_menu, root, door_card
from wanmark.models import MainMenuBot, SubMenuBot, DoorCardBot


async def main_menu_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    async for main_menu_one in MainMenuBot.objects.all():
        keyboard.add(InlineKeyboardButton(
            main_menu_one.name, callback_data=main_menu.new(m_id=main_menu_one.id))
        )
    return keyboard


async def sub_menu_kb(main_menu_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    async for submain_menu_one in SubMenuBot.objects.filter(link_main_menu=main_menu_id):
        keyboard.add(InlineKeyboardButton(
            submain_menu_one.name, callback_data=sub_menu.new(s_id=submain_menu_one.id))
        )
    keyboard.add(InlineKeyboardButton(
        'Назад', callback_data=root.new())
    )
    return keyboard


async def door_card_kb(main_menu_id: int = None, sub_menu_id: int = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    if sub_menu_id:
        async for door_card_menu_one in DoorCardBot.objects.filter(link_submenu=sub_menu_id):
            keyboard.add(InlineKeyboardButton(
                door_card_menu_one.name, callback_data=door_card.new(d_id=door_card_menu_one.id))
            )
        keyboard.add(InlineKeyboardButton(
            'Назад', callback_data=main_menu.new(m_id=main_menu_id))
        )
    return keyboard


async def one_door_card_kb(
        main_menu_id: int = None,
        sub_menu_id: int = None,
        door_card_id: int = None
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    one_door_card: DoorCardBot = await DoorCardBot.objects.aget(id=door_card_id)
    keyboard.add(InlineKeyboardButton(
        'Установленные двери', callback_data=1)
    )
    keyboard.add(InlineKeyboardButton(
        'Назад', callback_data=sub_menu.new(s_id=sub_menu_id))
    )
    return keyboard
