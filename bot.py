from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, state
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import database as db

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

keyboard = None
phone_button = KeyboardButton('Прислать контакт')




@dp.message_handler(Command('start'))
async def hello_message(message: types.Message):
    await message.answer(
        text=f'Привет, {message.from_user.full_name}\nТы в моем чат-боте, если хочешь чек-лист, нажми на кнопку', )


@dp.message_handler()
async def check_list(message: types.Message):
    if message.text == 'Хочу чек-лист':
        if
        await message.answer(text='ffff', reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Хочу на вебинар ЕГЭ':
        await message.answer(text='ссылка на вебинар егэ')
    elif message.text == 'хочу на вебинар ОГЭ':
        await message.answer('ссылка на ОГЭ')


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def phone_query(message:):
    user_telephone_num = message.contact.phone_number

    await message.answer(f"Ваш номер телефон: {user_telephone_num}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
