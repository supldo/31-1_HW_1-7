# HW 6
# Aiogram
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# Bot
from config import bot
# Database
from database.sql_commands import Database
# Scraper
from parsel import Selector
import requests


# 1.0. Создать свой собственный скрапер для любого сайта из которого вы хотите парсить данные для пользователя
def requests_anime():
    xpath_anime_link = '//a[@class="cover anime-tooltip"]/@href'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8',
    }
    link = "https://shikimori.me/animes/kind/tv/status/ongoing"
    req_anime = requests.get(link, headers=headers).text
    tree = Selector(text=req_anime)
    return tree.xpath(xpath_anime_link).getall()


# 2.2. Когда вы высылаете посты или новости поочередна чтобы пользователь мог сохранить свой любимый пост в базу данных
class AnimeNews(StatesGroup):
    anime = State()


async def anime(message: types.Message, state: FSMContext):
    await AnimeNews.anime.set()
    async with state.proxy() as data:
        data['requests_anime'] = requests_anime()
        data['anime_num'] = 0
        data['anime'] = data['requests_anime'][data['anime_num']]
    await show_anime(message=message, anime=data['anime'])


# 2.2. Когда вы высылаете посты или новости поочередна чтобы пользователь мог сохранить свой любимый пост в базу данных
async def next_anime(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['anime_num'] = data['anime_num'] + 1
        data['anime'] = data['requests_anime'][data['anime_num']]
    if data['anime_num'] >= 5:
        await state.finish()
    else:
        await show_anime(message=call.message, anime=data['anime'])


async def show_anime(message, anime):
    markup_anime = InlineKeyboardMarkup()
    next_anime_btn = InlineKeyboardButton(
        "Следующая новость",
        callback_data="next_anime"
    )
    markup_anime.add(next_anime_btn)
    anime_note = InlineKeyboardButton(
        "Добавить в заметки",
        callback_data="save_anime_note"
    )
    markup_anime.add(anime_note)

    await bot.send_message(chat_id=message.chat.id, text=anime, reply_markup=markup_anime)


# 2.2. Когда вы высылаете посты или новости поочередна чтобы пользователь мог сохранить свой любимый пост в базу данных
async def save_anime_note(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        Database().sql_insert_scraper_note(call.from_user.id, data['anime'])
    await bot.send_message(chat_id=call.message.chat.id, text='Добавлено в заметки')


# 2.3. Выводить список новостей которые он сохранил в базе.
async def anime_note(message: types.Message):
    all_anime = Database().sql_select_scraper_note(message.from_user.id)
    for anime in all_anime:
        await bot.send_message(chat_id=message.chat.id, text=anime['link'])


def register_scrapers(dp: Dispatcher):
    # 1.1. Отправлять с помощью команды.
    dp.register_message_handler(anime, commands=['anime'])
    # 2.2. Когда вы высылаете посты или новости поочередна чтобы пользователь мог сохранить свой любимый пост в базу данных
    dp.register_callback_query_handler(next_anime, lambda call: call.data == "next_anime", state=AnimeNews)
    dp.register_callback_query_handler(save_anime_note, lambda call: call.data == "save_anime_note", state=AnimeNews)
    dp.register_message_handler(anime_note, commands=['anime_note'])
