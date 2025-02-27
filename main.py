from dotenv import load_dotenv
load_dotenv('.env')  # it's very important because there is some os.getenv calls in packages

import json
import logging.config

with open('logging_config.json') as f:
    logging_config = json.load(f)
logging.config.dictConfig(logging_config)

import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from periodic_parsing.scheduler import periodic_parsing_scheduler
from bot.bot import bot
from bot.handlers.menu_handlers import menu_router
from bot.dialogs import dialogs_router

logger = logging.getLogger('main')

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
setup_dialogs(dp)
dp.include_routers(
    dialogs_router,
    menu_router,
)


async def main():
    try:
        periodic_parsing_scheduler.start()
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical('Fatal error: %s', e, exc_info=True)


if __name__ == '__main__':
    logger.info('Bot started')
    while True:
        asyncio.run(main())
