from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from bot.utils.user_utils import is_registered, register_user, unregister_user
from bot.reply_templates.menu import START_TEMPLATE, HELP_TEMPLATE, STOP_TEMPLATE

menu_router = Router(name='menu')


@menu_router.message(Command('start'))
async def startup_answer(msg: Message):
    await msg.delete()
    await msg.answer(START_TEMPLATE, parse_mode='HTML')

    if not await is_registered(msg.from_user.id):
        await register_user(msg.from_user.id)


@menu_router.message(Command('help'))
async def help_answer(msg: Message):
    await msg.delete()
    await msg.answer(HELP_TEMPLATE, parse_mode='HTML')


@menu_router.message(Command('stop'))
async def stop_answer(msg: Message):
    await msg.delete()
    await msg.answer(STOP_TEMPLATE, parse_mode='HTML')

    await unregister_user(msg.from_user.id)
