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
    try:
        db.create_table()
    except Exception as err:
        print(err)

    full_name = message.from_user.full_name
    try:
        db.add_user(id=message.from_user.id, fullname=full_name)
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
        if db.check_phone(id=message.from_user.id) == "NULL":
            await message.answer(text='Тебя нет в базе')

            await message.answer(text='Для начала тебе надо зарегистрироваться в моем боте.\n'
                                      'Просто нажми на кнопку ниже.\n'
                                      'Не переживай, звонить не буду',
                                 reply_markup=kb.phone_kb)
    if message.text == 'бд':
        await message.answer(text=db.select_all_users())


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def phone_query(message: types.Message):
    """Ловим контакт пользователя и записываем его в БД"""
    user_phone_number = message.contact.phone_number
    db.update_user_phone(phone=user_phone_number, id=message.from_user.id)
    user_info = db.select_user(id=message.from_user.id)
    await message.answer(f"Ваш номер телефон: {user_phone_number}")
    await message.answer(f'Запись в БД: {user_info}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
