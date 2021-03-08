from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

check_list_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                    keyboard=[
                                        [
                                            KeyboardButton(text="Хочу чек-лист")
                                        ]
                                    ])
phone_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                                   [
                                       KeyboardButton(text="📱",
                                                      request_contact=True)
                                   ]
                               ])
