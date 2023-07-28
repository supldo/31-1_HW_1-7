# Aiogram
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# Bot
from config import bot
# Database
from database.sql_commands import Database
# Scraper
from parsel import Selector
import requests

def requests_news():
    xpath_news = '///a[@class="name"]/@href'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8',
    }
    link = f"https://shikimori.me/forum/news"
    requests_news = requests.get(link, headers=headers).text
    news = Selector(text=requests_news)
    anime_news = news.xpath(xpath_news).getall()
    return anime_news


class AnimeNews(StatesGroup):
    news_1 = State()
    news_2 = State()
    news_3 = State()
    news_4 = State()
    news_5 = State()

async def anime_news_1(message: types.Message, state: FSMContext):
    await AnimeNews.news_1.set()
    async with state.proxy() as data:
        data['news'] = requests_news()
    text = f'{data["news"][0]}\nОтправьте любое слово чтоб продолжить'
    await message.reply(text=text)
    await AnimeNews.next()


async def next_anime_news_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['news'] = requests_news()
    text = f'{data["news"][1]}\nОтправьте любое слово чтоб продолжить'
    await message.reply(text=text)
    await AnimeNews.next()


async def next_anime_news_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['news'] = requests_news()
    text = f'{data["news"][2]}\nОтправьте любое слово чтоб продолжить'
    await message.reply(text=text)
    await AnimeNews.next()


async def next_anime_news_4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['news'] = requests_news()
    text = f'{data["news"][3]}\nОтправьте любое слово чтоб продолжить'
    await message.reply(text=text)
    await AnimeNews.next()


async def next_anime_news_5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['news'] = requests_news()
    text = f'{data["news"][4]}\nОтправьте любое слово чтоб продолжить'
    await message.reply(text=text)
    await AnimeNews.next()


def register_scrapers(dp: Dispatcher):
    dp.register_message_handler(anime_news_1, commands=['anime_news'])
    dp.register_message_handler(next_anime_news_2, state=AnimeNews.news_2, content_types=['text'])
    dp.register_message_handler(next_anime_news_3, state=AnimeNews.news_3, content_types=['text'])
    dp.register_message_handler(next_anime_news_4, state=AnimeNews.news_4, content_types=['text'])
    dp.register_message_handler(next_anime_news_5, state=AnimeNews.news_5, content_types=['text'])