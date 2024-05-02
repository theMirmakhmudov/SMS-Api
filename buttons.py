from aiogram import types

kb = [
    [types.KeyboardButton(text="SMS Yuborish ✉️")]
]
keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, selective=True,
                                      input_field_placeholder="SMS Yuborish uchun bosing")

kb2 = [
    [types.KeyboardButton(text="Share Contact 👤", request_contact=True)]
]
keyboard2 = types.ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True, selective=True,
                                      input_field_placeholder="Contact ulashish uchun bosing")
