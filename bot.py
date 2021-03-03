from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import sqlite3

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

check_list = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='Хочу чек-лист')]])


@dp.message_handler(Command('start'))
async def hello_message(message: types.Message):

    await message.answer(text=f'Привет, {message.from_user.full_name}\nТы в моем чат-боте, если хочешь чек-лист, нажми на кнопку', )


@dp.message_handler()
async def check_list(message: types.Message):
    if message.text == 'Хочу чек-лист':
        await message.answer(text='ffff', reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Хочу на вебинар ЕГЭ':
        await message.answer(text='ссылка на вебинар егэ')
    elif message.text == 'хочу на вебинар ОГЭ':
        await message.answer('ссылка на ОГЭ')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
