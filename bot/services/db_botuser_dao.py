import logging

from telebot.types import Chat, User

from bot.models import BotUser

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
        logger.info(f'Успешно создан пользователь в БД {data.id} {username} {full_name}')
    else:
        logger.info(f'Успешно обновлен пользователь в БД {data.id} {username} {full_name}')
    return create_status
