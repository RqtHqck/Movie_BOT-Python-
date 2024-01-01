from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ikb_make():
    inl_keyboard = InlineKeyboardMarkup(row_width=1)
    _1 = InlineKeyboardButton(text='text_1', callback_data='1x')
    _2 = InlineKeyboardButton(text='text_2', callback_data='2x')
    _3 = InlineKeyboardButton(text='text_3', callback_data='3x')
    return inl_keyboard.add(_1, _2, _3)
