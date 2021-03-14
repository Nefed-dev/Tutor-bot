from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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
                                       KeyboardButton(text="Пройти регистрацию в боте 📱",
                                                      request_contact=True)
                                   ]
                               ])
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                    keyboard=[
                                        [KeyboardButton(text='Хочу чек-лист')],
                                        [KeyboardButton(text='Хочу на вебинар')],
                                        [KeyboardButton(text='Интенсив ОГЭ')]

                                    ])

vebinar_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                       keyboard=[
                                           [KeyboardButton(text='Вебинар ОГЭ')],
                                           [KeyboardButton(text='Вебинар ЕГЭ')],
                                           [KeyboardButton(text='Назад')]
                                       ])