from aiogram import Bot, Dispatcher, executor, types
from buttons import main_kb, confirm_kb
from database_functions import make_database, add_user, change_screen, get_screen
from config import API_TOKEN
from data_validation import check_phone
from constants import *
import json

make_database()

users_messages = {}

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types='text')
async def handle_messages(messages: types.Message):
    message = json.loads(str(messages))
    is_bot = message['from']['is_bot']
    if not is_bot:
        user_id = message['from']['id']
        chat_id = message['chat']['id']
        add_user(user_id, chat_id)
        if message.get('text') is not None:
            msg_text = message['text']
            if get_screen(user_id) == START_SCREEN:
                if msg_text.lower() == '/help' or msg_text.lower() == 'помощь❓':
                    await bot.send_message(chat_id=chat_id, text=HELP_MSG, reply_markup=main_kb,
                                           disable_web_page_preview=True)
                    change_screen(user_id, START_SCREEN)
                    users_messages[user_id] = {}
                elif msg_text.lower() == '/start' or msg_text.lower() == 'начать🏁':
                    await bot.send_message(chat_id=chat_id, text=START_MSG, reply_markup=main_kb,
                                           disable_web_page_preview=True)
                    change_screen(user_id, START_SCREEN)
                    users_messages[user_id] = {}
                elif msg_text.lower() == '/message' or msg_text.lower() == 'отправка сообщения✉':
                    await bot.send_message(chat_id=chat_id, text=SENDER_MSG_1, reply_markup=types.ReplyKeyboardRemove(),
                                           disable_web_page_preview=True)
                    change_screen(user_id, SEND_MESSAGE_FIRST_STAGE_SCREEN)
                    users_messages[user_id] = {}
            elif get_screen(user_id) != START_SCREEN:
                if get_screen(user_id) == SEND_MESSAGE_FIRST_STAGE_SCREEN:
                    if check_phone(msg_text):
                        users_messages[user_id]["phone_number"] = msg_text
                        await bot.send_message(chat_id=chat_id, text=SENDER_MSG_2,
                                               reply_markup=types.ReplyKeyboardRemove(),
                                               disable_web_page_preview=True)
                        change_screen(user_id, SEND_MESSAGE_SECOND_STAGE_SCREEN)
                    else:
                        await bot.send_message(chat_id=chat_id, text=SENDER_ERROR_MSG,
                                               reply_markup=main_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, START_SCREEN)
                elif get_screen(user_id) == SEND_MESSAGE_SECOND_STAGE_SCREEN:
                    users_messages[user_id]["message_text"] = msg_text
                    check_msg = f"Данные корректны?\n" \
                                f"Номер телефона:\n{users_messages[user_id]['phone_number']}\n" \
                                f"Сообщение для отправки:\n{users_messages[user_id]['message_text']}"
                    await bot.send_message(chat_id=chat_id, text=check_msg,
                                               reply_markup=confirm_kb,
                                               disable_web_page_preview=True)
                    change_screen(user_id, SEND_MESSAGE_CONFIRM_SCREEN)
                elif get_screen(user_id) == SEND_MESSAGE_CONFIRM_SCREEN:
                    if msg_text == "Да✅":
                        # Do smth to send sms message
                        pass
                    await bot.send_message(chat_id=chat_id, text=CHOOSE_ACTION_MSG, reply_markup=main_kb,
                                           disable_web_page_preview=True)
                    change_screen(user_id, START_SCREEN)
                    users_messages[user_id] = {}

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
