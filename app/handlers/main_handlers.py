from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BadRequest, ChatNotFound

from core.poll_validate import poll_validator
from create_bot import bot
from api import anime_api, currency_api, weather_api
from keyboards import else_or_cancel_kb, menu_keyboard, multifunc_kb