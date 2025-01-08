import os
import asyncio
from traceback import print_exception
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from periodic_parsing.scheduler import periodic_parsing_scheduler
from bot.handlers.menu_handlers import menu_router

load_dotenv('.env')
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_routers(
    menu_router,
)


async def main():
    try:
        periodic_parsing_scheduler.start()
        await dp.start_polling(bot)
    except Exception as e:
        print_exception(e)


if __name__ == '__main__':
    print('Bot started')
    while True:
        asyncio.run(main())
