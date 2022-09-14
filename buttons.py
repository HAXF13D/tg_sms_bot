from aiogram import types
from aiogram.types import KeyboardButton as KeyBut

start_btn = KeyBut('Начать🏁')
help_btn = KeyBut('Помощь❓')
msg_send_btn = KeyBut('Отправка сообщения✉')

yes_btn =KeyBut('Да✅')
no_btn =KeyBut('Нет🚫')

main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).row(
    start_btn).row(
    help_btn).row(
    msg_send_btn)

confirm_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    yes_btn, no_btn
)



print()