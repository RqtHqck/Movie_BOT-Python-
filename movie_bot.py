# For_Aiogram
from aiogram import Bot, Dispatcher, executor, types
from config import token_API
# Keyboards
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# Imported IKB
from ikb import ikb_make

bot = Bot(token=token_API)
dp = Dispatcher(bot)

help_text = 's'


async def on_startup(_):
    # Говорит, что бот запущен
    print('Bot is polling')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        text='Hi there👋. You can choose any of the bot features available below. If you want to learn about the commands of this bot, press /help',
        reply_markup=ikb_make())


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer(
        text=help_text)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True)
