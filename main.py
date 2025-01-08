from dotenv import load_dotenv
load_dotenv('.env')  # it's very important because there is some os.getenv calls in packages

import asyncio
from traceback import print_exception
from aiogram import Dispatcher
from periodic_parsing.scheduler import periodic_parsing_scheduler
from bot.bot import bot
from bot.handlers.menu_handlers import menu_router

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
