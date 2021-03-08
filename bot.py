from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, state
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import sqlite3
from database import Database
import keyboard as kb

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
db = Database(path_to_db="users.db")
phone_button = KeyboardButton('Прислать контакт')


@dp.message_handler(Command('start'))
async def hello_message(message: types.Message):
    """Ловим стартовое сообщение от пользователя"""
    '''Здороваемся с пользователем, отправляем клавиатуру с возможностями'''

    full_name = message.from_user.full_name
    try:
        db.add_user(id=message.from_user.id, name=full_name, phone=1)
    except sqlite3.IntegrityError as err:
        print(err)
    await message.answer(
        text=f'{full_name} Привет!\nТы в моем чат-боте, если хочешь чек-лист, нажми на кнопку',
        reply_markup=kb.check_list_kb)


@dp.message_handler()
async def check_list(message: types.Message):
    """Ловим текстовые сообщения"""
    '''Ловим сообщения с обычных кнопок и отвечаем на них'''

    if message.text == "Хочу чек-лист":
        # Если пользователя нет в базе данных, запросить его номер телефона
        await message.answer(text='Для начала тебе надо зарегистрироваться в моем боте.\n'
                                  'Просто нажми на кнопку ниже.\n'
                                  'Не переживай, звонить не буду',
                             reply_markup=kb.phone_kb)

        # Если пользователь есть в базе данных, прислать ему чек-лист


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def phone_query(message: types.Message):
    """Ловим контакт пользователя и записываем его в БД"""
    user_telephone_number = message.contact.phone_number
    await message.answer(f"Ваш номер телефон: {user_telephone_number}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
