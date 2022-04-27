from aiogram import types
from aiogram.utils.markdown import hbold


def standard_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = ('Balance', 'Pools')
    keyboard.add(*(types.KeyboardButton(text) for text in buttons))
    return keyboard
