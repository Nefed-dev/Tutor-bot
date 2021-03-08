from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import Command
from aiogram import types
from bot import dp


@dp.message_handler(Command('start'))
async def hello_message(message: types.Message):
    user_id = message.message_id
    await message.answer(text=f'{user_id}')

@dp.m


@dp.message_handler()
async def check_list():
    pass

