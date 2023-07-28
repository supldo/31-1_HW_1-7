from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import Database
from datetime import datetime, timedelta

# Echo Ban  # hw2
async def echo_ban(message: types.Message):
    ban_words = ["bitch", "damn", "fuck"]
    if message.chat.type == 'supergroup' and message.text.lower().replace(" ", '') in ban_words:
        if Database().sql_select_user_ban(telegram_id=message.from_user.id, group_id=message.chat.id):
            text_ban = f"Пользователь {message.from_user.username} был ограничен к чату на 1 день!"
            ban_date = datetime.now() + timedelta(days=1)
            await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, until_date=ban_date)
            await bot.send_message(chat_id=message.chat.id, text=text_ban)
        else:
            text_warning = "Предупреждение! Использование ненормативной лексики в чате, ограничивается доступ к чату!"
            await bot.send_message(chat_id=message.chat.id, text=text_warning)
        Database().sql_insert_user_ban(telegram_id=message.from_user.id,
                                       group_id=message.chat.id,
                                       reasons=message.text.lower().replace(" ", ''))
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


def register_echo_ban(dp: Dispatcher):
    dp.register_message_handler(echo_ban)