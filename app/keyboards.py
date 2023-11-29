from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup

multi_kb = InlineKeyboardMarkup(row_width=1)

button_weather = InlineKeyboardButton(text='Узнать текущию погоду', 
                                      callback_data="Weather")

button_currency = InlineKeyboardButton(text='Конвектор валют', 
                                      callback_data="Wallet")

button_anime = InlineKeyboardButton(text='Отправь "Няшку"', 
                                      callback_data="Anime")

button_cancel = InlineKeyboardButton(text='Отмена',
                                     callback_data='Back')

(multi_kb.add(button_weather)
)
multi_kb.add(button_cancel)


# Создание основной клавиатуры
button_funcs = KeyboardButton('Функционал')

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

menu_keyboard.add(button_funcs)

# клавиатура повторить попытку/отмена
else_or_cancel_kb = InlineKeyboardMarkup()
repeat_button = InlineKeyboardButton(text='Повторить',
                                     callback_data='Repeat')
else_or_cancel_kb.add(button_cancel).add(repeat_button)