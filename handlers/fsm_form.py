# Aiogram
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# Bot
from config import bot
# Database
from database.sql_commands import Database


class FormStates(StatesGroup):
    idea = State()
    problems = State()
    assessment = State()

async def fsm_start(message: types.Message):
    await message.reply("Идея")
    await FormStates.idea.set()

async def load_idea(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['idea'] = message.text
    await FormStates.next()
    await message.reply("Проблемы")

async def load_problems(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['problems'] = message.text
    await FormStates.next()
    await message.reply("Оценка бота")
async def load_assessment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        Database().sql_insert_user_survey(
            idea=data['idea'],
            problems=data['problems'],
            assessment=message.text,
            user_id=message.from_user.id
        )
        await state.finish()
    await message.reply("Успех!")


def register_handler_fsm_form(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['survey'])
    dp.register_message_handler(load_idea, state=FormStates.idea, content_types=['text'])
    dp.register_message_handler(load_problems, state=FormStates.problems, content_types=['text'])
    dp.register_message_handler(load_assessment, state=FormStates.assessment, content_types=['text'])