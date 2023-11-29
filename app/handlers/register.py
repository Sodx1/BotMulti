from aiogram import Dispatcher
from handlers.main_handlers import (States, callback_type, else_or_cancel,
                                    funcs,
                                    weather, start_command,
                                    unknown)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands='start')
    dp.register_message_handler(funcs, text='Функционал')
    dp.register_message_handler(weather, state=States.weather)
    #dp.register_message_handler(currency_conversion,
    #                          state=States.currency_conversion)
    dp.register_message_handler(unknown)
    dp.register_callback_query_handler(callback_type,
                                       state=States.callback_type)
    dp.register_callback_query_handler(else_or_cancel,
                                       state=States.else_or_cancel)