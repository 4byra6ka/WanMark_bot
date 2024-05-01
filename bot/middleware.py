from abc import ABC

from telebot import BaseMiddleware

from bot.services.db_botuser_dao import update_or_create_tg_user


class CustomMiddleware(BaseMiddleware, ABC):
    def __init__(self):
        super(CustomMiddleware, self).__init__()
        self.update_sensitive = True
        self.update_types = ['message', 'edited_message']

    async def pre_process_message(self, message, data):
        # only message update here
        my_date = None
        message.step = ''
        try:
            my_date = getattr(message, 'chat')
        except AttributeError:
            pass
        try:
            my_date = getattr(message, 'from_user')
        except AttributeError:
            pass
        if not my_date:
            return None
        if not message.text:
            return None
        create_status = await update_or_create_tg_user(my_date)

    async def post_process_message(self, message, data, exception):
        pass # only message update here for post_process

    async def pre_process_edited_message(self, message, data):
        pass # only edited_message update here

    async def post_process_edited_message(self, message, data, exception):
        pass # only edited_message update here for post_process
