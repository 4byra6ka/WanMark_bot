from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.filters import main_menu, sub_menu, root, door_card, contact, application, subscription, install_door_card
from wanmark.models import MainMenuBot, SubMenuBot, DoorCardBot, SettingsBot, InstallDoorCardBot


async def main_menu_kb() -> InlineKeyboardMarkup:
    """Формирование кнопок для главного меню"""
    keyboard = InlineKeyboardMarkup()
    async for main_menu_one in MainMenuBot.objects.all():
        keyboard.add(InlineKeyboardButton(
            main_menu_one.name, callback_data=main_menu.new(m_id=main_menu_one.id))
        )
    first_settings_bot: SettingsBot = await SettingsBot.objects.afirst()
    if first_settings_bot:
        if first_settings_bot.on_contact:
            keyboard.add(InlineKeyboardButton(
                first_settings_bot.contact_button, callback_data=contact.new())
            )
        if first_settings_bot.on_application:
            keyboard.add(InlineKeyboardButton(
                first_settings_bot.application_button, callback_data=application.new())
            )
        if first_settings_bot.on_subscription:
            keyboard.add(InlineKeyboardButton(
                first_settings_bot.subscription_button, callback_data=subscription.new())
            )
    return keyboard


async def sub_menu_kb(main_menu_id: int) -> InlineKeyboardMarkup:
    """Формирование кнопок для подменю"""
    keyboard = InlineKeyboardMarkup()
    async for submain_menu_one in SubMenuBot.objects.filter(link_main_menu=main_menu_id):
        keyboard.add(InlineKeyboardButton(
            submain_menu_one.name, callback_data=sub_menu.new(s_id=submain_menu_one.id))
        )
    async for door_card_menu_one in DoorCardBot.objects.filter(link_main_menu=main_menu_id):
        keyboard.add(InlineKeyboardButton(
            door_card_menu_one.name, callback_data=door_card.new(d_id=door_card_menu_one.id, img=False))
        )
    keyboard.add(InlineKeyboardButton(
        'Назад', callback_data=root.new())
    )
    return keyboard


async def door_card_kb(main_menu_id: int = None, sub_menu_id: int = None) -> InlineKeyboardMarkup:
    """Формирование кнопок для списка дверей"""
    keyboard = InlineKeyboardMarkup()
    if sub_menu_id:
        async for door_card_menu_one in DoorCardBot.objects.filter(link_submenu=sub_menu_id):
            keyboard.add(InlineKeyboardButton(
                door_card_menu_one.name, callback_data=door_card.new(d_id=door_card_menu_one.id, img=False))
            )
        keyboard.add(InlineKeyboardButton(
            'Назад', callback_data=main_menu.new(m_id=main_menu_id))
        )
    return keyboard


async def install_door_card_kb(door_card_id: int = None) -> InlineKeyboardMarkup:
    """Формирование кнопок для списка установленных дверей"""
    keyboard = InlineKeyboardMarkup()
    if door_card_id:
        async for install_door_card_menu_one in InstallDoorCardBot.objects.filter(link_door_card=door_card_id):
            keyboard.add(InlineKeyboardButton(
                install_door_card_menu_one.name, callback_data=install_door_card.new(id_id=install_door_card_menu_one.id))
            )
        keyboard.add(InlineKeyboardButton(
            'Назад', callback_data=door_card.new(d_id=door_card_id, img=False))
        )
    return keyboard


async def one_door_card_kb(
        main_menu_id: int = None,
        sub_menu_id: int = None,
        door_card_id: int = None,
        door_img: bool = False
) -> InlineKeyboardMarkup:
    """Формирование кнопок для двери и установленной двери"""
    keyboard = InlineKeyboardMarkup()
    if not door_img:
        keyboard.add(InlineKeyboardButton(
            'Живые фото дверей', callback_data=door_card.new(d_id=door_card_id, img=True))
        )
        if sub_menu_id:
            keyboard.add(InlineKeyboardButton(
                'Назад', callback_data=sub_menu.new(s_id=sub_menu_id))
            )
        else:
            keyboard.add(InlineKeyboardButton(
                'Назад', callback_data=main_menu.new(m_id=main_menu_id))
            )
    else:
        keyboard.add(InlineKeyboardButton(
            'Назад', callback_data=door_card.new(d_id=door_card_id, img=False))
        )
    return keyboard


async def back_main_menu_kb(
        name_button: str = 'Назад',
) -> InlineKeyboardMarkup:
    """Формирование кнопки назад в главное меню"""
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        name_button, callback_data=root.new())
    )
    return keyboard


async def no_address_kb(
        name_button: str = 'Пропустить ввод адреса',
) -> InlineKeyboardMarkup:
    """Формирование кнопки назад в главное меню"""
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        name_button, callback_data='no_address')
    )
    keyboard.add(InlineKeyboardButton(
        'Отмена заявки', callback_data=root.new())
    )
    return keyboard


async def back_install_door_card_kb(
        name_button: str = 'Назад',
        door_card_id: int = None
) -> InlineKeyboardMarkup:
    """Формирование кнопки назад в установленные двери"""
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        name_button, callback_data=door_card.new(d_id=door_card_id, img=True))
    )
    return keyboard
