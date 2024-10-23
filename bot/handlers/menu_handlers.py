from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

menu_router = Router(name='menu')


# TODO: write answers texts
@menu_router.message(Command('start', 'help'))
async def startup_answer(msg: Message):
    await msg.delete()
    await msg.answer('Start command answer text')

