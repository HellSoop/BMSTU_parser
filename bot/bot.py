import os
from aiogram import Bot

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
