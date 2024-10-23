import os
import datetime
import asyncio
from pyrogram import Client
from dotenv import load_dotenv
from base_classes import AsyncAbstractParser

load_dotenv('../.env')
TG_API_ID = os.getenv('TG_USER_API_ID')
TG_API_HASH = os.getenv('TG_USER_API_HASH')


# TODO: Create in TGParser method that extracts all valuable data from output posts for the final response
# TODO: Make TGParser return all photo/video appeared at the same time as single post
class TGParser(AsyncAbstractParser):
    MAX_POSTS = 60  # I suppose that fewer than 60 posts appear in the channel per hour
    NEW_POSTS_TIME = datetime.timedelta(hours=1)

    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    async def parse(self):
        """
        Parse posts from the channel determined by `self.channel`. self.MAX_POSTS posts will be returned.
        :return: List of posts parsed from the channel.
        """
        async with Client("my_account", TG_API_ID, TG_API_HASH) as client:
            posts = [post async for post in client.get_chat_history(self.channel, limit=self.MAX_POSTS)]

            return posts

    async def parse_new(self):
        """
        Parse posts from the channel determined by `self.channel`. self.MAX_POSTS posts will be returned.
        Only posts that appeared within self.NEW_POSTS_TIME before the method call will be returned.
        :return: Filtered list of posts parsed from the channel.
        """
        since_datetime = datetime.datetime.now() - self.NEW_POSTS_TIME

        async with Client("my_account", TG_API_ID, TG_API_HASH) as client:
            posts = [post async for post in client.get_chat_history(self.channel, limit=self.MAX_POSTS)
                     if post.edit_date >= since_datetime]

            return posts


if __name__ == '__main__':  # DEBUG! Don't forget to remove!
    async def main():
        photo_id = (await parser.parse())[0].photo
        print(photo_id)


    parser = TGParser(channel='b2b_bmstu')
    asyncio.run(main())
