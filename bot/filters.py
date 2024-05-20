from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import AdvancedCustomFilter, StateFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.types import CallbackQuery


main_menu = CallbackData('m_id', prefix='main')
sub_menu = CallbackData('s_id', prefix='sub')
door_card = CallbackData('d_id', 'img', prefix='door')
root = CallbackData(prefix='root')


class MainMenuCBFilter(AdvancedCustomFilter):
    key = 'main_menu_config'

    async def check(self, call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class SubMenuCBFilter(AdvancedCustomFilter):
    key = 'sub_menu_config'

    async def check(self, call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class DoorCardCBFilter(AdvancedCustomFilter):
    key = 'door_card_config'

    async def check(self, call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class RootCBFilter(AdvancedCustomFilter):
    key = 'root_config'

    async def check(self, call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


def bind_filters(bot: AsyncTeleBot):
    bot.add_custom_filter(MainMenuCBFilter())
    bot.add_custom_filter(SubMenuCBFilter())
    bot.add_custom_filter(DoorCardCBFilter())
    bot.add_custom_filter(RootCBFilter())
    bot.add_custom_filter(StateFilter(bot))
