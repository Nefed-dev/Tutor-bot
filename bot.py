from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command

from config import BOT_TOKEN
from database import Database
import keyboard as kb
import sqlite3

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
db = Database(path_to_db='users.db')

CHECK_LIST_LINK = 'https://drive.google.com/file/d/1Q48SJJM4GYQGx22JKBUinBk3HBfnD0my/view?usp=sharing'


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

    await message.answer(text=f'{user_fullname}, привет. Сначала зарегистрируйся. '
                              f'Это просто защита от спама. Не переживай звонить не буду',
                         reply_markup=kb.phone_kb)


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

    await message.answer(text='Круто! Теперь ты зарегистрирован в моем боте! \n'
                              'Нажми на одну из предложенных ниже кнопок и ты полчишь своё!',
                         reply_markup=kb.main_keyboard)

    user_info = db.select_user(id=message.from_user.id)

    await dp.bot.send_message(chat_id=335825375, text=f"Новый зарегистрированный в Dema Fizmat: \n{user_info}, phone=={user_phone}")


@dp.message_handler()
async def message_answer(message: types.Message):
    # user_info = db.select_user(id=message.from_user.id)
    #
    # await dp.bot.send_message(chat_id=335825375, text=f"Новый зарегистрированный в Dema Fizmat: \n{user_info}")

    if message.text == 'Хочу чек-лист':
        await message.answer(text=f'Держи. Чек лист находится по ссылке :)\n'
                                  f'{CHECK_LIST_LINK}')
    elif message.text == 'Хочу на вебинар':
        await message.answer(text='Отлично! Для получения ссылки нажми на ЕГЭ или ОГЭ',
                             reply_markup=kb.vebinar_keyboard)
    elif message.text == 'Интенсив по ОГЭ':
        await message.answer(
            text='Скоро будет что-то интересное! \n'
                 'Следи за инстой, также я пришлю информацию через бота')
    elif message.text == 'Назад':
        await message.answer(text='Нажми на одну из предложенных ниже кнопок и ты полчишь своё!',
                             reply_markup=kb.main_keyboard)
    elif message.text == 'Вебинар ОГЭ':
        await message.answer(text='Просто перейди по ссылке и ты попадешь в чат по вебинару\n'
                                  'https://t.me/joinchat/H8rY12S3o_HvJeuM')
    elif message.text == 'Вебинар ЕГЭ':
        await message.answer(text='Просто перейди по ссылке и ты попадешь в чат по вебинару ЕГЭ\n'
                                  'https://t.me/joinchat/WBHiBNDvLwKIDc6T')
    elif message.text == 'Интенсив ОГЭ':
        await message.answer(text='Привет, я готовлю бомбовый интенсив по подготовке к ОГЭ, '
                                  'где ты за 20 часов научишься писать ОГЭ на стабильную четверку, '
                                  'либо подтянуть свою оценку до Пятерки!\n '
                                  'Следи за сторис, также я пришлю информацию в этот бот')
    # else:
    #     await message.answer(reply_markup=kb.main_keyboard,
    #                          text='Бот не принимает другие сообщения. Нажми на одну из предложенных кнопок')


if __name__ == '__main__':
    try:
        db.create_table()
    except Exception as err:
        print(err)

    executor.start_polling(dp, skip_updates=True)
