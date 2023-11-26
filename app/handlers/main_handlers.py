from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BadRequest, ChatNotFound


from create_bot import bot
from api import anime_api, currency_api, weather_api
from keyboards import else_or_cancel_kb, menu_keyboard, multifunc_kb

class States(StatesGroup):
    """
    Создаем состояние для бота
    """
    callback_type = State()
    weather = State()
    currency_conversion = State()
    else_or_cancel = State()

async def funcs(message: types.Message):
    """
    Обработчик показывающий функционал бота
    """
    await message.answer('Выбери что тебя интересует',
                         reply_markup=multifunc_kb)
    await States.callback_type.set()