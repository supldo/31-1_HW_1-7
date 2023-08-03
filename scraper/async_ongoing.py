from aiogram import Dispatcher, types

from config import bot

from database.sql_commands import Database

from parsel import Selector
import requests
import asyncio
import httpx


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8',
}


class AsyncNewsScraper:
    def __init__(self):
        self.urls = []

    START_URL = "https://shikimori.me/animes/kind/tv/status/ongoing/score/6"
    START_URL_PAGES = START_URL + "/page/{}"
    LINK_XPATH = '//a[@class="cover anime-tooltip"]/@href'


    async def get_url(self, client, url):
        response = await client.get(url)
        await self.parse_links(response.text)
        return response


    async def parse_links(self, content):
        tree = Selector(text=content)
        urls = tree.xpath(self.LINK_XPATH).extract()
        self.urls.append(urls)


    async def parse_data(self):
        timeout = httpx.Timeout(50.8)
        async with httpx.AsyncClient(headers=DEFAULT_HEADERS, timeout=timeout) as client:
            tasks = [asyncio.create_task(self.get_url(client, self.START_URL))]
            for page in range(2, 5):
                tasks.append(asyncio.create_task(self.get_url(client, self.START_URL_PAGES.format(page))))
            new_gather = await asyncio.gather(*tasks)
            await client.aclose()
        return self.urls


async def ongoing(message: types.Message):
    scraper = AsyncNewsScraper()
    urls = []
    urls_list = await scraper.parse_data()
    for url in urls_list:
        urls.extend(url)
    for i in range(0, 5):
        await bot.send_message(chat_id=message.chat.id, text=urls[i])


def register_scrapers_ongoing(dp: Dispatcher):
    dp.register_message_handler(ongoing, commands=['top_ongoing'])
