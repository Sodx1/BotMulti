from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from create_bot import bot
from api import anime_api, currency_api, weather_api
from keyboards import else_or_cancel_kb, menu_keyboard, multi_kb

class States(StatesGroup):
    """
    Создаем состояние для бота
    """
    callback_type = State()
    weather = State()
    currency_conversion = State()
    else_or_cancel = State()

async def start_command(message: types.Message):
    """
    Обработка команды /start
    """

    await message.answer(f'Привет, {message.from_user.first_name}.',
                         reply_markup=menu_keyboard)

async def funcs(message: types.Message):
    """
    Обработчик показывающий функционал бота
    """
    await message.answer('Выбери что тебя интересует',
                         reply_markup=multi_kb)
    await States.callback_type.set()

async def callback_type(callback_query: types.CallbackQuery,
                        state:FSMContext):
    """
    Обработчик callback при выборе функции
    """
    async with state.proxy() as data:
        data['type_callback'] = callback_query.data
    if data['type_callback'] == 'Weather':
        await callback_query.message.answer('Напишите город, в котором хотите'
                                            ' узнать погоду:')
        await States.weather.set()
    elif data['type_callback'] == 'Wallet':
        await callback_query.message.answer('Напишите валюту и сумму в '
                                            'формате FROM:TO:AMOUNT'
                                            '(Пример USD:RUB:1)')
        await States.currency_conversion.set()
    else:
        await state.finish()
    await callback_query.message.delete()


async def weather(message: types.Message, state: FSMContext):
    """
    Обработчик погоды
    """ 
    weather = await weather_api.get_weather(message.text)

    if weather['cod'] == 200:
        city = weather['name']
        temp = weather['main']['temp']
        description = weather['weather'][0]['description']
        feels_like = weather['main']['feels_like']
        temp_min = weather['main']['temp_min']
        temp_max = weather['main']['temp_max']
        wind_speed = weather['wind']['speed']
        weather_message = (f'Погода в городе: {city}\n'
                           f'Погодные условия: {description}\n'
                           f'Температура: {temp}\n'
                           f'Ощущается: {feels_like}\n'
                           f'Минимальная температура: {temp_min}\n'
                           f'Максимальная температура: {temp_max}\n'
                           f'Скорость ветра: {wind_speed} м\с\n'
                           )
        await message.answer(weather_message)
        await state.finish()
    elif weather['cod'] == 'server_error':
        await message.reply('Сервер не отвечает :(')
        await state.finish()
    elif weather['cod'] == '404':
        await message.reply('К сожалению, такой город не найден :(',
                            reply_markup=else_or_cancel_kb)
        await States.else_or_cancel.set()
async def else_or_cancel(callback_query: types.CallbackQuery,
                         state: FSMContext):
    """
    Обработчик колбэка с отмена/повторить
    """

    async with state.proxy() as data:
        data['else_or_cancel'] = callback_query.data
    if data['else_or_cancel'] == 'Back':
        if data['type_callback'] == 'Weather':
            await States.weather.set()
            await callback_query.message.answer('Введите название города еще '
                                                'раз:')

    await callback_query.message.delete()



async def unknown(message: types.Message):
    """
    Обработка неизвестных команд/сообщений
    """
    await message.reply('Неизвестная команда')