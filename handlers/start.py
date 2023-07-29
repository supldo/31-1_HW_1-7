# Import
from const import HELP_TEXT
# Aiogram
from aiogram import types, Dispatcher
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup    # hw1
from aiogram.utils.deep_linking import _create_link    # hw5
# Database
from database.sql_commands import Database
# Bot
from config import bot
# Keyboards
from keyboards import start_keyboard
# Moduls
from random import randint    # hw1
from datetime import datetime, timedelta
from binascii import hexlify    # hw5
from os import urandom    # hw5


# Start
async def start_button(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    Database().sql_insert_user_table_query(telegram_id=telegram_id,
                                           username=username,
                                           first_name=first_name,
                                           last_name=last_name)

    await message.reply(text=f"Hello {message.from_user.username}!",
                        reply_markup=start_keyboard.start_keyboard())

    Database().sql_insert_wallet(telegram_id)    # hw5
    await referral_check(message)   # hw5


# Help
async def help_button(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_TEXT)


# Quiz   # hw1   # 2.0.
quiz_id = None
async def quiz_1(message: types.Message):
    global quiz_id
    quiz_id = 'quiz_1'
    question = "Вопрос 1"
    option = [
        "Вариант 1",
        "Вариант 2",
        "Вариант 3",
        "Вариант 4"
    ]
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "Следующая викторина",
        callback_data="button_call_1"
    )
    markup.add(button_call_1)
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=option,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Правильный ответ 2",
        explanation_parse_mode=types.ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )
async def quiz_2(call: types.PollAnswer):
    global quiz_id
    quiz_id = 'quiz_2'
    question = "Вопрос 2"
    option = [
        "Вариант 1",
        "Вариант 2",
        "Вариант 3",
        "Вариант 4"
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=option,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Правильный ответ 3",
        explanation_parse_mode=types.ParseMode.MARKDOWN_V2
    )
# hw1   # 3.1.
async def handle_poll_answer(poll_answer: types.PollAnswer):
    Database().sql_insert_quiz(telegram_id=poll_answer.user.id,
                               quiz=quiz_id,
                               quiz_option=poll_answer.option_ids[0])


# Random   # hw1
async def random(message: types.Message):
    rand_num = randint(1, 100)
    await message.reply(text=rand_num)


# Жалоба   # hw4
async def complaint(message: types.Message):
    complaint_text = message.text.split()

    if len(complaint_text) > 1:
        bad_username = complaint_text[1]
        telegram_id = int(message.from_user.id)
        telegram_id_bad_user = Database().sql_select_id_by_username(bad_username)[0]['username']
        reason = complaint_text[2:] if len(complaint_text) >= 3 else ''
        count = 1
        complaint_check = Database().sql_select_complaint_check(user_id=telegram_id, bad_user_id=telegram_id_bad_user).fetchall()

        if complaint_check:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Вы уже отправляли жалобу на {bad_username}')
        elif telegram_id_bad_user == telegram_id:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Не стоит на себя жаловатся! 🙃')
        elif telegram_id_bad_user:
            Database().sql_insert_complaint(telegram_id=telegram_id,
                                            telegram_id_bad_user=telegram_id_bad_user,
                                            reason=reason,
                                            count=count)

            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Отправлено жалоба на {bad_username}')

            count_complaint = len(Database().sql_select_complaint(user_id=telegram_id_bad_user).fetchall())
            if count_complaint >= 3:
                await bot.send_message(chat_id=telegram_id_bad_user,
                                       text=f'На вас 3 раза пожаловались. '
                                            f'Вы исключены из группы Supido Group!')
                ban_date = datetime.now() + timedelta(days=365)
                await bot.ban_chat_member(message.chat.id, telegram_id_bad_user, ban_date)
            else:
                await bot.send_message(chat_id=telegram_id_bad_user,
                                       text=f'На вас пожаловались. '
                                            f'Ещё {3 - count_complaint} жалоба и вас исключат из группы!')
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Такой пользователь не найден')


# Реферальная ссылка   # hw5
async def reference_link(message: types.Message):
    link_exist = Database().sql_select_user_return_link(telegram_id=message.from_user.id)
    link = link_exist[0]["link"]
    if link:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"У тебя уже есть реферальная ссылка!\n"
                                    f"Ссылка: {link}")
    else:
        code = hexlify(urandom(4)).decode()
        link = await _create_link(link_type="start", payload=code)
        Database().sql_update_user_reference_link(link=link, telegram_id=message.from_user.id)
        await bot.send_message(message.from_user.id,
                               f"Твоя реферальная ссылка: {link}")


# Проверка реферальной ссылки   # hw5
async def referral_check(message: types.Message):

    if len(message.text.split()) > 1:
        referral = message.text.split()[1]
        user_id = Database().sql_select_user_by_link(f'%{referral}')[0]['link']
        if user_id == message.from_user.id:
            await bot.send_message(message.chat.id, 'Нельзя приглашать самого себя! 🙃')
        elif not Database().sql_select_referral(message.from_user.id):
            Database().sql_insert_referral(user_id, message.from_user.id)
            Database().sql_update_wallet(user_id, 100)
            await bot.send_message(user_id, f'Пользователь зашёл через вашу реферальную ссылку, к вам зачислено +100 баллов\n'
                                            f'Свои баллы можете посмотреть через команду: /wallet')


# Список рефералов   # hw5
async def referrals(message: types.Message):
    referrals = Database().sql_select_all_referrals(message.from_user.id)
    if referrals:
        show_referrals = ''
        count_referrals = 0
        for referral in referrals:
            user_n = lambda x: x if x is not None else ""
            count_referrals += 1
            referral_list = [f"{count_referrals}:",
                             user_n(referral['username']),
                             user_n(referral['first_name']),
                             user_n(referral['last_name'])]
            referral_str = ' '.join(referral_list)
            show_referrals += referral_str
        await bot.send_message(message.chat.id, show_referrals)
    else:
        await bot.send_message(message.chat.id, 'У вас пока нету рефералов')


# Кошелёк   # hw5
async def wallet(message: types.Message):
    point = Database().sql_select_wallet(message.from_user.id)
    await message.reply(f'На вашем счету: {point} баллов')


# Dispatcher
def register_handlers(dp: Dispatcher):

    # Start
    dp.register_message_handler(start_button, commands=['start'])

    # Help
    dp.register_message_handler(help_button, commands=['help'])

    # Quiz    # hw1
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
    dp.register_poll_answer_handler(handle_poll_answer)

    # Random    # hw2
    dp.register_message_handler(random, commands=['random'])

    # Complaint    # hw4
    dp.register_message_handler(complaint, commands=['complaint'])

    # Reference Link    # hw5
    dp.register_message_handler(reference_link, commands=['reference'])

    # Referrals list   # hw5
    dp.register_message_handler(referrals, commands=['referrals'])

    # Wallet   # hw5
    dp.register_message_handler(wallet, commands=['wallet'])