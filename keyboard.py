from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

"""Основная клавиатура с предложением услуг"""
check_list_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                    keyboard=[
                                        [
                                            KeyboardButton(text="Хочу чек-лист")
                                        ]
                                    ])

"""Вспомогательная клавиатура с кнопокй, запрашивающей номер телефона"""
phone_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                                   [
                                       KeyboardButton(text="📱",
                                                      request_contact=True)
                                   ]
                               ])
