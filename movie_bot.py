# AIOGRAM======================================================================================
from aiogram import Bot, Dispatcher, executor, types
from config import token_API
# Keyboards
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# Imported IKB
from ikb import ikb_make

# LAST YEAR====================================================================================
from kinogo_last_year_f import find_5films_lastyear
from kinogo_last_year_s import find_5serials_lastyear
from kinogo_recom_film import recommend_film
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# RANDOM=======================================================================================
import random

bot = Bot(token=token_API)
dp = Dispatcher(bot)

help_text = '<b>/start</b> - Запустить бота\n' + '<em>Команды внутри бота\n</em>' + "<b>Порекомендовать новинку</b> - Попросить бота порекомендовать один из новых фильмов\n" + "<b>Фильмы за год</b> - Фильмы за последний год\n" + "<b>Сериалы за год</b> - Сериалы за последний год\n" + '<b>Ссылка на сайт</b> - Ссылка на сайт Kinogo'


async def on_startup(_):
    # Говорит, что бот запущен
    print('Bot is polling')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        text='Привет👋. Вы можете выбрать одну из кнопок ниже. Учтите, что бот использует сайт <b>kinogo</b> для поиска фильмов для Вас. ' +
             'Если Вы хотите узнать о командах этого бота, нажмите /help. Ссылку на сайт <b>kinogo</b>Вы тоже можете найти там.',
        reply_markup=ikb_make(),
        parse_mode='HTML')


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer(
        text=help_text,
        parse_mode='HTML')


@dp.callback_query_handler()
async def buttons(callback: types.CallbackQuery):
    if callback.data == 'Recommend':
        recommeded_film = recommend_film()
        keys = (list(recommeded_film.keys()))
        for key in keys:
            name = key
            country = recommeded_film[key][0]
            link = recommeded_film[key][1]
            description = recommeded_film[key][2]
            photo = recommeded_film[key][3]

            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=photo,
                                 caption=f'<b>Название:</b> {name},\n<b>Страна:</b> {country},\n<b>Описание:</b> {description}\n<b>Ссылка:</b> {link}',
                                 parse_mode='HTML')
            await callback.message.answer(text='Приятного просмотра!😊')

    elif callback.data == 'Year_f':
        last_year_films_dict = find_5films_lastyear()

        keys = (list(last_year_films_dict.keys()))
        print(len(keys))
        random_keys = random.sample(keys, 3)
        print(random_keys)
        for key in random_keys:
            name = key
            country = last_year_films_dict[key][0]
            link = last_year_films_dict[key][1]
            description = last_year_films_dict[key][2]
            photo = last_year_films_dict[key][3]

            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=photo,
                                 caption=f'<b>Название:</b> {name},\n<b>Страна:</b> {country},\n<b>Описание:</b> {description}\n<b>Ссылка:</b> {link}',
                                 parse_mode='HTML')
            await callback.message.answer(text='Приятного просмотра!😊')

    elif callback.data == 'Year_s':
        last_year_serials_dict = find_5serials_lastyear()

        keys = (list(last_year_serials_dict.keys()))
        print(len(keys))
        random_keys = random.sample(keys, 3)
        print(random_keys)
        for key in random_keys:
            name = key
            country = last_year_serials_dict[key][0]
            link = last_year_serials_dict[key][1]
            description = last_year_serials_dict[key][2]
            photo = last_year_serials_dict[key][3]

            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=photo,
                                 caption=f'<b>Название:</b> {name},\n<b>Страна:</b> {country},\n<b>Описание:</b> {description}\n<b>Ссылка:</b> {link}',
                                 parse_mode='HTML')
            await callback.message.answer(text='Приятного просмотра!😊')

    elif callback.data == 'link':
        await callback.message.answer(text='Вот ссылка на сайт kinogo https://kinogo.biz,\nПриятного просмотра!😁')


@dp.message_handler()
async def all_messages(message):
    await message.answer(
        text='Пожалуйста, используйте какую-либо команду из существующих, либо нажмите /help, чтобы открть справочник.')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True)
