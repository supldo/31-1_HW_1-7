from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage    # hw3

# HW3
admin = [
    931619695,
    6314725426,
    421124124
]

storage = MemoryStorage()                   # hw3
TOKEN = config('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)   # hw3 storage=storage
