import logging

from telebot.types import Chat, User, InputMediaPhoto

from bot.models import BotUser, MenuActions
from wanmark.models import DoorCardBot, ImageTitleDoorCardBot, SettingsBot, ImageInstallDoorCardBot

logger = logging.getLogger(__name__)


async def update_or_create_tg_user(data: Chat | User):
    try:
        data = getattr(data, 'chat')
    except AttributeError:
        data = data
    username = data.username
    if not data.username:
        username = None
    full_name = data.full_name
    if not data.full_name:
        full_name = None
    defaults_dict = {
        'username': username,
        'full_name': full_name,
        'status_active': True
    }
    telegram_user, create_status = await BotUser.objects.aupdate_or_create(telegram_id=data.id, defaults=defaults_dict)
    if create_status:
        logger.info(f'{telegram_user.telegram_id} Успешно создан пользователь в БД {data.id} {username} {full_name}')
    else:
        logger.info(f'{telegram_user.telegram_id} Успешно обновлен пользователь в БД {data.id} {username} {full_name}')
    return create_status


async def update_or_create_menu_actions(
        telegram_id: int,
        main_id: int = None,
        main: bool = None,
        sub_id: int | str = None,
        sub: bool = None,
        door_id: int = None,
        door: bool = None,
        message_id: int = None,
        message: bool = False,
        media_message_id: str = None,
        media_message: bool = False,
):
    bot_user: BotUser = await BotUser.objects.aget(telegram_id=telegram_id)
    defaults = {}
    create_defaults = {'main': None, 'sub': None, 'door': None, 'message_id': None, 'media_message_id': None}
    if main_id or main:
        defaults['main'] = main_id
        create_defaults['main'] = main_id
    if sub_id or sub:
        defaults['sub'] = sub_id
        create_defaults['sub'] = sub_id
    if door_id or door:
        defaults['door'] = door_id
        create_defaults['door'] = door_id
    if message_id or message:
        defaults['message_id'] = message_id
        create_defaults['message_id'] = message_id
    if media_message_id or media_message:
        defaults['media_message_id'] = media_message_id
        create_defaults['media_message_id'] = media_message_id
    menu_actions, create_status = await MenuActions.objects.aupdate_or_create(
        bot_user=bot_user,
        defaults=defaults,
        create_defaults=create_defaults
    )
    if create_status:
        logger.info(f'{bot_user.telegram_id} Успешно создано состояние меню в БД {create_defaults}')
    else:
        logger.info(f'{bot_user.telegram_id} Успешно обновлен состояние меню в БД {defaults}')
    return create_status


async def get_menu_actions(telegram_id: int):
    bot_user: BotUser = await BotUser.objects.aget(telegram_id=telegram_id)
    try:
        menu_actions: MenuActions = await MenuActions.objects.aget(bot_user=bot_user)
        result = {'main': menu_actions.main, 'sub': menu_actions.sub, 'door': menu_actions.door,
                  'message_id': menu_actions.message_id, 'media_message_id': menu_actions.media_message_id}
        logger.info(f'{bot_user.telegram_id} Успешно создан запрос состояния меню в БД {result}')
        return result
    except MenuActions.DoesNotExist:
        logger.info(f'{bot_user.telegram_id} Нету состояния меню в БД')
        await update_or_create_menu_actions(telegram_id)
        menu_actions: MenuActions = await MenuActions.objects.aget(bot_user=bot_user)
        result = {'main': menu_actions.main, 'sub': menu_actions.sub, 'door': menu_actions.door,
                  'message_id': menu_actions.message_id, 'media_message_id': menu_actions.media_message_id}
        logger.info(f'{bot_user.telegram_id} Успешно создан запрос состояния меню в БД {result}')
        return result
        # return None


async def get_image_title_door(door_card: DoorCardBot, img: bool = False) -> list:
    list_list_image = []
    list_image = []
    if not img:
        async for door_card_title_image in ImageTitleDoorCardBot.objects.filter(link_door_card=door_card):
            list_image.append(InputMediaPhoto(door_card_title_image.image.read()))
            if len(list_image) == 10:
                list_list_image.append(list_image)
        else:
            list_list_image.append(list_image)
    else:
        async for door_card_install_image in ImageInstallDoorCardBot.objects.filter(link_door_card=door_card):
            list_image.append(InputMediaPhoto(door_card_install_image.image.read()))
            if len(list_image) == 10:
                list_list_image.append(list_image)
        else:
            list_list_image.append(list_image)
    return list_list_image


async def get_description_main_menu():
    first_des_main_menu: SettingsBot = await SettingsBot.objects.afirst()
    if first_des_main_menu is not None:
        title = first_des_main_menu.main_title
        image = first_des_main_menu.main_image.read()
        return title, image
    with open('static/no-image-icon.png', 'rb') as rf:
        image = rf.read()
    return None, image


async def get_contact() -> str:
    first_des_contact: SettingsBot = await SettingsBot.objects.afirst()
    if first_des_contact is not None:
        name = first_des_contact.contact_button if first_des_contact.contact_button else '...'
        title = first_des_contact.contact_title if first_des_contact.contact_title else '...'
        return f'{name}\n{title}'
    return '...'
