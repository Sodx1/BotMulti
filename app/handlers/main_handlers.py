from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from api import currency_api, weather_api
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


async def currency_conversion(message: types.Message, state: FSMContext):
    """
    Обработчик конвертации валют
    """
    
    data ={}
    text = message.text.split(':')
    if len(text) !=3:
        await message.reply('Данные введены в неверном формате.',
                            reply_markup=else_or_cancel_kb)
        await States.else_or_cancel.set()
    else:
        data.update({'from': text[0], 'to': text[1], 'amount': text[2]})
        wait_message = await message.answer('Ожидание ответа сервера...')
        conversion = await currency_api.get_conversion(data)
        await wait_message.delete()
        if conversion.get('error'):
            if conversion['error'] == 'server_error':
                await message.reply('К сожалению сервер не отвечает :(')
                await state.finish()
                return
            elif conversion['error']['code'] == 401:
                await message.reply(
                    f'Введена некоректная валюта FROM ({text[0]}).',
                    reply_markup=else_or_cancel_kb
                )
            elif conversion['error']['code'] == 402:
                await message.reply(
                    f'Введена некоректная валюта TO ({text[1]}).',
                    reply_markup=else_or_cancel_kb
                )
            elif conversion['error']['code'] == 403:
                await message.answer(
                    f'Введено некоректное число AMOUNT ({text[2]}).',
                    reply_markup=else_or_cancel_kb
                )
            await States.else_or_cancel.set()
        elif conversion.get('success'):
            result = conversion['result']
            date = datetime.fromtimestamp(conversion['info']['timestamp'])
            to_currency = data['to'].upper()
            from_currency = data['from'].upper()
            amount = data['amount']
            conversion_message = (
                f'Конвертация валюты прошла успешно!\n'
                f'Валюты: {from_currency} -> {to_currency}\n'
                f'Количество денег: {amount} {from_currency}\n'
                f'Результат: {result:.2f} {to_currency}\n'
                f'Дата конвертации: {date}'
            )
            await message.answer(conversion_message)
            await state.finish()

async def else_or_cancel(callback_query: types.CallbackQuery,
                         state: FSMContext):
    """
    Обработчик колбэка с отмена/повторить
    """

    async with state.proxy() as data:
        data['else_or_cancel'] = callback_query.data
    if data['else_or_cancel'] == 'Back':
        await state.finish()
        if data['type_callback'] == 'Weather':
            await States.weather.set()
            await callback_query.message.answer('Введите название города еще '
                                                'раз:')
        elif data['type_callback'] == 'Wallet':
            await States.currency_conversion.set()
            await callback_query.message.answer('Введите данные для'
                                                ' конвертации еще раз:')

    await callback_query.message.delete()



async def unknown(message: types.Message):
    """
    Обработка неизвестных команд/сообщений
    """
    await message.reply('Неизвестная команда')