import os
import datetime
import asyncio
from pyrogram import Client
from dotenv import load_dotenv
from base_classes import AsyncAbstractParser

load_dotenv('../.env')
TG_API_ID = os.getenv('TG_API_ID')
TG_API_HASH = os.getenv('TG_API_HASH')


class TGParser(AsyncAbstractParser):
    MAX_POSTS = 100
    NEW_POSTS_TIME = datetime.timedelta(hours=1)

    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    async def parse(self):
        async with Client("my_account", TG_API_ID, TG_API_HASH) as client:
            posts = [post async for post in client.get_chat_history(self.channel, limit=self.MAX_POSTS)]

            return posts

    async def parse_new(self):
        since_datetime = datetime.datetime.now() - self.NEW_POSTS_TIME

        async with Client("my_account", TG_API_ID, TG_API_HASH) as client:
            posts = [post async for post in client.get_chat_history(
                self.channel,
                limit=self.MAX_POSTS,
                offset_date=since_datetime,
                offset=-self.MAX_POSTS)]

            return posts


if __name__ == '__main__':  # DEBUG! Don't forget to remove!
    async def main():
        print(await parser.parse_new())


    parser = TGParser(channel='studsovet_bmstu')
    asyncio.run(main())
