from aiogram.utils import executor
from config import dp
from handlers import start, echo_ban, fsm_form  # hw1   # hw2   # hw3
from scraper import scraper_news, async_ongoing # hw6
from admin import start_admin
from database import sql_commands

start.register_handlers(dp=dp)                  # hw1
start_admin.register_handlers_admin(dp=dp)      # hw1
fsm_form.register_handler_fsm_form(dp=dp)       # hw3
scraper_news.register_scrapers(dp=dp)           # hw6
echo_ban.register_echo_ban(dp=dp)               # hw2
async_ongoing.register_scrapers_ongoing(dp=dp)  # hw7

async def on_startup(_):
    db = sql_commands.Database()
    db.sql_create_user_table_query()
    print("Bot is ready")

if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup
                           )