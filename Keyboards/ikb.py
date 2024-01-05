from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ikb_make():
    inl_keyboard = InlineKeyboardMarkup(row_width=2)
    _1_films = InlineKeyboardButton(text='Фильмы за год', callback_data='Year_f')
    _1_serials = InlineKeyboardButton(text='Сериалы за год', callback_data='Year_s')
    _2_recomend = InlineKeyboardButton(text='Порекомендовать новинку', callback_data='Recommend')
    _3_link_on_site = InlineKeyboardButton(text='Ссылка на Kinogo', callback_data='link')
    return inl_keyboard.add(_2_recomend).add(_1_films, _1_serials).add(_3_link_on_site)
