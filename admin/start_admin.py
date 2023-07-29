# Aiogram
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# Database
from database.sql_commands import Database
# Bot
from config import bot, admin

# Функции админа
async def secret_word(message: types.Message):
    if message.from_user.id in admin and message.chat.type != 'supergroup':
        markup = InlineKeyboardMarkup()
        button_call_1 = InlineKeyboardButton("Список пользователей",
                                             callback_data="list_of_users")
        markup.add(button_call_1)
        button_call_2 = InlineKeyboardButton("Список потенциальных пользователей на бан",
                                             callback_data="list_potential_user_ban")
        markup.add(button_call_2)
        button_call_3 = InlineKeyboardButton("Список опросов",
                                             callback_data="list_user_survey")
        markup.add(button_call_3)
        await message.reply("Master", reply_markup=markup)



# Список пользователей   # hw2
async def list_of_users(call: types.CallbackQuery):
    users = Database().sql_select_user_table_query()
    if users:
        for user in users:
            await bot.send_message(call.message.chat.id,
                                   f'ID: {user["telegram_id"]}\n'
                                   f'Пользователь: {user["username"]}\n'
                                   f'Имя: {user["first_name"]}\n'
                                   f'Фамилия: {user["last_name"]}')
    else:
        await bot.send_message(call.message.chat.id, "Список пуст")


# Список потенциальных на бан   # hw2
async def list_potential_user_ban(call: types.CallbackQuery):
    users = Database().sql_select_potential_user_ban()
    if users:
        for user in users:
            await bot.send_message(call.message.chat.id,
                                   f'ID: {user["telegram_id"]}\n'
                                   f'Пользователь: {user["username"]}\n'
                                   f'Имя: {user["first_name"]}\n'
                                   f'Фамилия: {user["last_name"]}\n'
                                   f'Причина: {user["reasons"]}')
    else:
        await bot.send_message(call.message.chat.id, "Список пуст")


# Список опросов    # HW3
class SurveyStates(StatesGroup):
    survey = State()
async def list_user_survey(call: types.CallbackQuery):
    surveys = Database().sql_select_user_survey()
    for survey in surveys:
        await bot.send_message(call.message.chat.id,
                               f'ID Опроса: {survey["id"]}\n'
                               f'Идея: {survey["idea"]}\n'
                               f'Проблемы: {survey["problems"]}\n'
                               f'Оценка: {survey["assessment"]}\n'
                               f'ID Пользователя: {survey["user_id"]}')
    await bot.send_message(call.message.chat.id, "Выберите опрос по ID")
    await SurveyStates.survey.set()


# Выбор опроса по ID    # HW3
async def load_survey(message: types.Message, state: FSMContext):
    id_survey = int(message.text)
    survey = Database().sql_select_user_survey_by_id(id_survey)[0]
    if survey:
        msg_result = f'ID Опроса: {survey["id"]}\n'\
                     f'Идея: {survey["idea"]}\n'\
                     f'Проблема: {survey["problems"]}\n'\
                     f'Оценка бота: {survey["assessment"]}\n'\
                     f'Пользователь: {survey["username"]}\n'\
                     f'Имя: {survey["first_name"]}\n'\
                     f'Фамилия: {survey["last_name"]}\n'\
                     f'ID Пользователя: {survey["telegram_id"]}'
        await message.reply(msg_result)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Нечего не найдено!')


# Диспетчер
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(secret_word, lambda word: "Ringo" in word.text)                                         # hw2
    dp.register_callback_query_handler(list_of_users, lambda call: call.data == "list_of_users")                        # hw2
    dp.register_callback_query_handler(list_potential_user_ban, lambda call: call.data == "list_potential_user_ban")    # hw2
    dp.register_callback_query_handler(list_user_survey, lambda call: call.data == "list_user_survey")                  # hw3
    dp.register_message_handler(load_survey, state=SurveyStates.survey, content_types=['text'])                         # hw3