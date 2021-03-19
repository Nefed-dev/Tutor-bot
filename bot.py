from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile

from config import BOT_TOKEN, ADMIN_ID
from database import Database
import keyboard as kb
import sqlite3

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
db = Database(path_to_db='users.db')

CHECK_LIST_LINK = 'https://drive.google.com/file/d/1Q48SJJM4GYQGx22JKBUinBk3HBfnD0my/view?usp=sharing'
EGE_CHAT_LINK = 'https://t.me/joinchat/WBHiBNDvLwKIDc6T'
OGE_CHAT_LINK = 'https://t.me/joinchat/H8rY12S3o_HvJeuM'


async def set_default_commands(dp):
    await dp.bot.set_my_commands([types.BotCommand("start", 'Запустить бота')])


def return_all_user():

    all_user = f'Всего в базе {db.count_users()[0]} человек.\n' \
               'Список всех зарегистрированных: \n' \
               'CHAT_ID - ИМЯ - НОМЕР ТЕЛЕФОНА\n'
    for user in db.select_all_users():
        all_user += f"{user[0]} - {user[1]} - {user[2]}\n"
    return all_user


@dp.message_handler(Command('start'))
async def hello_message(message: types.Message):
    """Ловим приветственное сообщение от пользователя, предлагаем ему кнопку отправить номер контакта"""
    user_fullname = message.from_user.full_name
    user_id = message.from_user.id

    try:
        db.create_table()
    except Exception as err:
        print(err)

    try:
        db.add_user(id=user_id, fullname=user_fullname)
    except sqlite3.IntegrityError as err:
        print(err)

    await message.answer(text=f'Привет! 😊\n\n'
                              f'Сначала зарегистрируйся 👌\n\n'
                              f'Телефон нужно ввести, чтобы система отправила тебе материал, звонить не буду, обещаю 😁',
                         reply_markup=kb.phone_kb)


@dp.message_handler(Command('dbinchat', prefixes='!'))
async def admin_db_in_chat(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        all_user = return_all_user()
        await message.answer(text=f'{all_user}')


@dp.message_handler(Command('dbdownload', prefixes='!'))
async def admin_db_download(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        bd_file = InputFile("users.db", filename="users.db")
        await bot.send_document(chat_id=user_id, document=bd_file)


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def registration(message: types.Message):
    """Ловим контакт пользователя,
    записываем в БД,
    присылаем клавиатуру с остальными функциями
    """

    user_phone = message.contact.phone_number

    try:
        db.update_user_phone(phone=user_phone, id=message.from_user.id)
    except sqlite3.InternalError as err:
        print(err)

    await message.answer(text='Супер! 😉 Теперь ты зарегистрирован в моем боте.\n\n'
                              'Нажми на одну из предложенных ниже кнопок и выбери, что ты хочешь получить',
                         reply_markup=kb.main_keyboard)

    user_info = db.select_user(id=message.from_user.id)
    # user_info = (id, name, phone)

    await dp.bot.send_message(chat_id=335825375, text=f"Новый зарегистрированный в Dema Fizmat: \n"
                                                      f"ID = {user_info[0]}\n"
                                                      f"Имя = {user_info[1]}, \n"
                                                      f"phone = {user_info[2]}")


@dp.message_handler()
async def message_answer(message: types.Message):
    if message.text == 'Хочу чек-лист':
        await message.answer(text=f'Держи 😉. \nЧек лист находится по ссылке :)\n'
                                  f'{CHECK_LIST_LINK}')
    elif message.text == 'Хочу на вебинар':
        await message.answer(text='Отлично! Нажми на одну из этих кнопок, и я скину тебе ссылку на соответствующий чат'
                                  '\n\nВся информация о предстоящих вебинарах будет там 😌',
                             reply_markup=kb.vebinar_keyboard)
    elif message.text == '⏪Назад⏪':
        await message.answer(text='Нажми на одну из предложенных ниже кнопок и выбери, что ты хочешь получить!',
                             reply_markup=kb.main_keyboard)
    elif message.text == 'Вебинар ОГЭ':
        await message.answer(text=f'Просто перейди по ссылке, и ты попадешь в чат по вебинару для ОГЭ\n'
                                  f'{OGE_CHAT_LINK}')
    elif message.text == 'Вебинар ЕГЭ':
        await message.answer(text=f'Просто перейди по ссылке, и ты попадешь в чат по вебинару для ЕГЭ\n'
                                  f'{EGE_CHAT_LINK}')


# elif message.text == 'Интенсив по ОГЭ':
#     await message.answer(
#         text='Скоро будет что-то интересное! \n'
#              'Следи за инстой, также я пришлю информацию через бота')
# elif message.text == 'Интенсив ОГЭ':
#     await message.answer(text='Привет, я готовлю бомбовый интенсив по подготовке к ОГЭ, '
#                               'где ты за 20 часов научишься писать ОГЭ на стабильную четверку, '
#                               'либо подтянуть свою оценку до Пятерки!\n '
#                               'Следи за сторис, также я пришлю информацию в этот бот')
# else:
#     await message.answer(reply_markup=kb.main_keyboard,
#                          text='Бот не принимает другие сообщения. Нажми на одну из предложенных кнопок')

async def on_startup(dp):
    try:
        db.create_table()
    except Exception as err:
        print(err)
    await set_default_commands(dp)

if __name__ == '__main__':

    executor.start_polling(dp, on_startup=on_startup)
