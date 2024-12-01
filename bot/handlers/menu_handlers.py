from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

menu_router = Router(name='menu')


# TODO: write answers texts
@menu_router.message(Command('start', 'help'))
async def startup_answer(msg: Message):
    # await msg.delete()
    # await msg.answer('Start command answer text')
    await msg.answer_photo(r'https://sun9-63.userapi.com/s/v1/ig2/zJjNFkh6vMY8ci5DHV4yi5ITEg15gKaW5KNOvebeovBXE6VyFiImtyI42NDC5HBYRihuG_CWVlDdMkSFo-0Zwc_h.jpg?quality=95&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640,720x720,756x756&from=bu')
